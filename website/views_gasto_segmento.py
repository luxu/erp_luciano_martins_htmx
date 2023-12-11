import json
import re
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from accounts.constants import MESES
from tools.utils import add_one_month, change_comma_by_dot
from vendor.cruds_adminlte.crud import CRUDView

from . import forms_gasto_segmento as form
from . import models_gasto_segmento as model


class GastosListView(LoginRequiredMixin, generic.ListView):
    model = model.Gasto
    template_name = "website/gasto/gastos_list.html"
    context_object_name = "gastos"
    paginate_by = 10
    ordering = ["-datagasto", "-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["count"] = self.get_queryset().count()
        except Exception:
            context["count"] = 0
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()
        if search := self.request.GET.get("search"):
            RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")
            # Essa linha qdo quero trazer o ID
            if RE_INT.match(search):
                queryset = queryset.filter(id=search)
            else:
                filters |= Q(name__icontains=search)
                filters |= Q(more_infos__icontains=search)
                filters |= Q(description_on_invoice__icontains=search)
                queryset = queryset.filter(filters)

        return queryset


class GastosCreateView(generic.CreateView):
    model = model.Gasto
    template_name = "website/gasto/gasto_form.html"
    form_class = form.GastoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = form.GastoForm(self.request.POST)
            context["formset"] = form.ParcelasFormSet(self.request.POST)
        else:
            context["forms"] = form.GastoForm()
            context["formset"] = form.ParcelasFormSet()
            context["last_data"] = (
                model.Gasto.objects.all().order_by("-datagasto").first()
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["forms"]
        formset = context["formset"]
        validated = forms.is_valid()
        if not formset.is_valid() or not validated:
            return self.render_to_response(self.get_context_data(form=form))
        gasto = forms.save(commit=False)
        total = 0.00
        for price in formset.cleaned_data:
            if len(price) > 0:
                vlr_parcela = price["valor_parcela"]
                if "." in vlr_parcela:
                    vlr_parcela = vlr_parcela.replace(".", "")
                total += float(vlr_parcela.replace(",", "."))
        gasto.total = round(total, 2)
        gasto.save()
        formset.instance = gasto
        formset.save()
        return redirect("website_gasto_list")


class GastosEditView(generic.UpdateView):
    model = model.Gasto
    template_name = "website/gasto/gasto_form.html"
    form_class = form.GastoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = form.GastoForm(self.request.POST, instance=self.object)
            context["formset"] = form.ParcelasFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["forms"] = form.GastoForm(instance=self.object)
            context["formset"] = form.ParcelasFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["forms"]
        formset = context["formset"]
        validated = forms.is_valid()
        if not formset.is_valid() or not validated:
            return self.render_to_response(self.get_context_data(form=form))
        gasto = forms.save(commit=False)
        total = 0.00
        for price in formset.cleaned_data:
            if len(price) > 0:
                total += float(price["valor_parcela"].replace(",", "."))
        gasto.total = round(total, 2)
        gasto.save()
        formset.instance = gasto
        formset.save()
        return redirect("website_gasto_list")


class GastosDeleteView(generic.DeleteView):
    success_url = reverse_lazy("website_gasto_list")
    model = model.Gasto
    template_name_suffix = "/gastos_confirm_delete"


class SegmentoCRUD(CRUDView):
    model = model.Segmento
    template_name_base = "ccruds"
    template_father = "principal/base.html"
    namespace = None
    check_perms = True
    views_available = ["create", "list", "delete", "update"]
    list_fields = [
        "name",
    ]
    search_fields = ["name__icontains"]
    split_space_search = " "  # default False
    add_form = form.SegmentoForm
    update_form = form.SegmentoForm


@login_required
def GastosPorMesView(request):
    template = "website/gasto/gastosPorMes.html"
    if request.method == "POST":
        context = _extracted_from_GastosPorMesView_4(request)
    else:
        segmentos = model.Segmento.objects.all()
        context = {"segmentos": segmentos}
    return render(request, template, context)


# TODO Rename this here and in `GastosPorMesView`
def _extracted_from_GastosPorMesView_4(request):
    dtInicial = request.POST.get("dtInicial")
    dtFinal = request.POST.get("dtFinal")
    today = datetime.today()
    """Se não vier com os campos date preenchidos
        será setado as datas de inicio e fim do mês corrente"""
    if dtInicial == "":
        dtInicial = datetime(today.year, today.month + 1, 1)
    if dtFinal == "":
        dtFinal = datetime(today.year, today.month + 1, today.day)
    qs = model.Gasto.objects.select_related("parcelas")
    qs = qs.exclude(name__startswith="PIX")
    qs = qs.exclude(name__startswith="TED")
    qs = qs.exclude(name__startswith="OF")
    qs = qs.filter(parcelas_gasto__data_parcela__range=[dtInicial, dtFinal])
    qs = qs.annotate(
        data_parcela=F("parcelas_gasto__data_parcela"),
        valor_parcela=F("parcelas_gasto__valor_parcela"),
        parcelas=F("parcelas_gasto__parcelas"),
        numero_parcela=F("parcelas_gasto__numero_parcela"),
    )
    qs = qs.values("id", "name", "datagasto", "data_parcela", "valor_parcela")
    # qs = qs.order_by("-datagasto")
    qs = qs.order_by("valor_parcela")
    if not qs:
        return {"dtInicial": dtInicial, "dtFinal": dtFinal}
    segmento_id = int(request.POST.get("segmento_id"))
    if segmento_id > 0:
        qs = qs.filter(segmento_id=segmento_id)
    vlr_total = round(
        sum(float(change_comma_by_dot(valor["valor_parcela"])) for valor in qs),
        ndigits=2,
    )

    segmentos = model.Segmento.objects.all()

    return {
        "data": qs,
        "total": vlr_total,
        "segmentos": segmentos,
    }


@login_required
def GastoPorParcelasView(request):
    template = "website/gasto/gastosPorParcelas.html"
    if request.method == "POST":
        context = _extracted_from_GastoPorParcelasView_4(request)
    else:
        context = {"meses": MESES}
    return render(request, template, context)


# TODO Rename this here and in `GastoPorParcelasView`
def _extracted_from_GastoPorParcelasView_4(request):
    dtInicial = request.POST.get("dtInicial")
    dtFinal = request.POST.get("dtFinal")
    porMes = request.POST.get("porMes")
    today = datetime.today()
    columns = (
        "id",
        "name",
        "parcelas",
        "numero_parcela",
        "valor_parcela",
        "data_parcela",
    )
    """Se não vier com os campos date preenchidos
        será setado as datas de inicio e fim do mês corrente"""
    if int(porMes) > 0:
        """Se mês for 1 número concatena o zero antes"""
        if len(porMes) < 2:
            porMes = "".join(("0", str(porMes)))
        dtInicial = datetime(today.year, int(porMes), 1)
        """Se o mês for FEVEREIRO vai até dia 28"""
        if today.month == 2:
            dtFinal = datetime(today.year, today.month, 28)
        else:
            dtFinal = datetime(today.year, today.month, 30)
    if dtInicial == "":
        dtInicial = datetime(today.year, today.month, 1)
    if dtFinal == "":
        """Se o mês for FEVEREIRO vai até dia 28"""
        if today.month == 2:
            dtFinal = datetime(today.year, today.month, 28)
        else:
            dtFinal = datetime(today.year, today.month, 30)
    qs = model.Gasto.objects.filter(
        parcelas_gasto__parcelas__gt=1,
        parcelas_gasto__data_parcela__range=[dtInicial, dtFinal],
    )
    qs = qs.annotate(
        data_parcela=F("parcelas_gasto__data_parcela"),
        valor_parcela=F("parcelas_gasto__valor_parcela"),
        parcelas=F("parcelas_gasto__parcelas"),
        numero_parcela=F("parcelas_gasto__numero_parcela"),
    )
    qs = qs.values(
        "id",
        "name",
        "parcelas",
        "numero_parcela",
        "valor_parcela",
        "data_parcela",
    )
    qs = qs.order_by("parcelas_gasto__data_parcela")
    vlr_total = sum(float(change_comma_by_dot(valor["valor_parcela"])) for valor in qs)

    return {
        "data": qs,
        "columns": columns,
        "total": round(vlr_total, ndigits=2),
        "meses": MESES,
    }


@login_required
def GastoPorSegmentoView(request):
    template = "website/gasto/gastosPorSegmento.html"
    if request.method == "POST":
        context = _extracted_from_GastoPorSegmentoView_4(request)
    else:
        segmentos = model.Segmento.objects.all().order_by("id")
        context = {"segmentos": segmentos}
    return render(request, template, context)


# TODO Rename this here and in `GastoPorSegmentoView`
def _extracted_from_GastoPorSegmentoView_4(request):
    dtInicial = request.POST.get("dtInicial")
    dtFinal = request.POST.get("dtFinal")
    today = datetime.today()
    """Se não vier com os campos date preenchidos
        será setado as datas de inicio e fim do mês corrente"""
    if dtInicial == "":
        dtInicial = datetime(today.year, today.month + 1, 1)
    if dtFinal == "":
        dtFinal = datetime(today.year, today.month + 1, today.day)
    segmento_id = int(request.POST.get("segmento_id"))
    qs = model.Gasto.objects.select_related("segmento")
    qs = qs.filter(
        segmento_id=segmento_id,
        parcelas_gasto__data_parcela__range=[dtInicial, dtFinal],
    )
    qs = qs.annotate(
        data_parcela=F("parcelas_gasto__data_parcela"),
        valor_parcela=F("parcelas_gasto__valor_parcela"),
        parcelas=F("parcelas_gasto__parcelas"),
        numero_parcela=F("parcelas_gasto__numero_parcela"),
    )
    qs = qs.annotate(
        data_parcela=F("parcelas_gasto__data_parcela"),
        valor_parcela=F("parcelas_gasto__valor_parcela"),
        parcelas=F("parcelas_gasto__parcelas"),
        numero_parcela=F("parcelas_gasto__numero_parcela"),
    )
    qs = qs.values("id", "name", "datagasto", "data_parcela", "valor_parcela")
    qs = qs.order_by("-datagasto")
    # 3.080.88
    vlr_total = sum(float(valor["valor_parcela"].replace(",", ".")) for valor in qs)

    segmentos = model.Segmento.objects.all().order_by("id")
    return {
        "data": qs,
        "total": round(vlr_total, ndigits=2),
        "segmentos": segmentos,
    }


@login_required
def SubdividirSegmentosView(request):
    template = "website/gasto/subdividirSegmentos.html"
    segmentos = model.Segmento.objects.all()
    if request.method == "POST":
        context = _extracted_from_SubdividirSegmentosView_5(request, segmentos)
    else:
        context = {"segmentos": segmentos}
    return render(request, template, context)


# TODO Rename this here and in `SubdividirSegmentosView`
def _extracted_from_SubdividirSegmentosView_5(request, segmentos):
    dtInicial = request.POST.get("dtInicial")
    dtFinal = request.POST.get("dtFinal")
    """Se não vier com os campos date preenchidos
        será setado as datas de inicio e fim do mês corrente"""
    if dtInicial == "":
        dtInicial = datetime.now()
    else:
        # Qdo vem a data ela vem como str e precisamos paassa para o type datetime
        # já que qdo for mostrar no HTML ele espera datetime e não str
        dtInicial = datetime.strptime(dtInicial, "%Y-%m-%d")
    if dtFinal == "":
        dtFinal = add_one_month()
    else:
        # Qdo vem a data ela vem como str e precisamos paassa para o type datetime
        # já que qdo for mostrar no HTML ele espera datetime e não str
        dtFinal = datetime.strptime(dtFinal, "%Y-%m-%d")
    list_ids_segmentos = list(
        model.Segmento.objects.filter().values("id", "name").order_by("id")
    )

    list_segmentos = []
    dict_segmentos = {}
    for segmento in list_ids_segmentos:
        gastos_por_segmento = model.Gasto.objects.filter(
            segmento_id=segmento["id"],
            parcelas_gasto__data_parcela__range=[dtInicial, dtFinal],
        )
        if len(gastos_por_segmento) > 0:
            dict_segmentos["total"] = sum(
                [float(gastos.total) for gastos in gastos_por_segmento]
            )
            dict_segmentos[segmento["name"]] = len(gastos_por_segmento)
            list_segmentos.append(dict_segmentos)
    nv_dict = {
        i: dict_segmentos[i]
        for i in sorted(dict_segmentos, key=dict_segmentos.get, reverse=True)
    }

    result = {
        "data": nv_dict,
        "segmentos": segmentos,
        "data_inicial": dtInicial,
        "data_final": dtFinal,
    }
    return result


def DetailsSegmentoView(request, segmento_name):
    template_name = "website/gasto/detailsSegmento.html"
    context = {"segmento_name": segmento_name}
    return render(request, template_name, context)


class AutoCompleteView(generic.FormView):
    def get(self, request):
        results = []
        if q := request.GET.get("term", "").capitalize():
            gastos = (
                model.Gasto.objects.filter(name__icontains=q)
                .values("name")
                .order_by("name")
                .distinct()
            )
        else:
            gastos = model.Gasto.objects.all()
        for gasto in gastos:
            gasto_json = {"name": gasto["name"]}
            results.append(gasto_json)
        data = json.dumps(results)
        mimetype = "application/json"
        return HttpResponse(data, mimetype)


class CardbankListView(LoginRequiredMixin, generic.ListView):
    model = model.Cardbank
    template_name = "website/gasto/cartoes_list.html"
    paginate_by = 10
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()
        if search := self.request.GET.get("search"):
            RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")
            # Essa linha qdo quero trazer o ID
            if RE_INT.match(search):
                queryset = queryset.filter(id=search)
            else:
                filters |= Q(name__icontains=search)
                queryset = queryset.filter(filters)
        return queryset


class CardbankCreateView(generic.CreateView):
    model = model.Cardbank
    template_name = "website/gasto/cardbanck_form.html"
    form_class = form.CardbankForm
    success_url = reverse_lazy("website_cartoes_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = form.CardbankForm(self.request.POST)
        else:
            context["forms"] = form.CardbankForm()
        return context


class CardbankEditView(generic.UpdateView):
    model = model.Cardbank
    template_name = "website/gasto/cardbanck_form.html"
    form_class = form.CardbankForm
    success_url = reverse_lazy("website_cartoes_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = form.CardbankForm(
                self.request.POST, instance=self.object
            )
        else:
            context["forms"] = form.CardbankForm(instance=self.object)
        return context


class CardbankDeleteView(generic.DeleteView):
    model = model.Cardbank
    template_name = "website/gasto/cardbank_confirm_delete.html"
    success_url = reverse_lazy("website_cartoes_list")
