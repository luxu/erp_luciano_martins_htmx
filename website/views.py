import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

# from django.utils.encoding import force_text
from django.views import generic

from accounts import constants
from . import forms, models

# from .admin import ComercioResource
from .filters import PecasFilter


# import tablib
# from import_export.formats import base_formats
# from import_export.forms import ConfirmImportForm
# from scripts import chatgpt
# from vendor.cruds_adminlte.crud import CRUDView


# from .resources import PecasResource


#: import / export formats
# DEFAULT_FORMATS = (
#     base_formats.CSV,
#     base_formats.XLS,
#     base_formats.TSV,
#     base_formats.ODS,
#     base_formats.JSON,
#     base_formats.YAML,
#     base_formats.HTML,
# )
# formats = DEFAULT_FORMATS
# import_formats = [f for f in formats if f().can_import()]


class PecasListView(LoginRequiredMixin, generic.ListView):
    model = models.Pecas
    template_name = "website/pecas/pecas_list.html"
    paginate_by = 10

    def resolve_order_field(self, context):
        ordering_field = self.request.GET.get("o", "")
        ordering_asc = ""
        if ordering_field:
            # check if asc or desc
            ordering_asc = "-" not in ordering_field
        querystring = self.request.GET.urlencode()
        # clear actual order field by replace, it will be added by each field on template
        # ex: "{{ ordering_url }}&o={% if ordering_asc %}-{% endif %}some_field"
        querystring = querystring.replace(f"&o={ordering_field}", "")
        context["ordering_url"] = f"?{querystring}"
        context["ordering_asc"] = ordering_asc
        return context, ordering_field

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context, ordering_field = self.resolve_order_field(context)
        pecas_filter = PecasFilter(self.request.GET, queryset=self.get_queryset())
        object_list = (
            pecas_filter.qs.order_by(ordering_field)
            if ordering_field
            else pecas_filter.qs
        )

        paginator = Paginator(object_list, self.paginate_by)
        page = self.request.GET.get("page")

        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        context["object_list"] = object_list

        context["filter"] = pecas_filter
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()

        if search := self.request.GET.get("search"):
            RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")
            # Essa linha qdo quero trazer o ID
            if RE_INT.match(search):
                filters |= Q(id=search)
            filters |= Q(comercio__description__icontains=search)
            filters |= Q(itenspecas__description__icontains=search)

        if type_vehicle := self.request.GET.get("type_vehicle"):
            filters |= Q(veiculo=type_vehicle)

        return queryset.filter(filters)


class PecasCreateView(generic.CreateView):
    model = models.Pecas
    template_name = "website/pecas/pecas_create.html"
    form_class = forms.PecasForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["form"] = forms.PecasForm(self.request.POST)
            context["formset"] = forms.ItemPecasFormSet(self.request.POST)
        else:
            context["form"] = forms.PecasForm()
            context["formset"] = forms.ItemPecasFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["form"]
        formset = context["formset"]
        validated = forms.is_valid()
        if not formset.is_valid() or not validated:
            return self.render_to_response(self.get_context_data(form=form))
        pecas = forms.save(commit=False)
        total = 0.00
        for price in formset.cleaned_data:
            total += float(price["subtotal"].replace(",", "."))
        pecas.total = round(total, 2)
        pecas.save()
        formset.instance = pecas
        formset.save()
        return redirect("website_pecas_list")


class PecasEditView(generic.UpdateView):
    model = models.Pecas
    template_name = "website/pecas/pecas_edit.html"
    form_class = forms.PecasForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = forms.PecasForm(self.request.POST, instance=self.object)
            context["formset"] = forms.ItemPecasFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["forms"] = forms.PecasForm(instance=self.object)
            context["formset"] = forms.ItemPecasFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["forms"]
        formset = context["formset"]
        validated = forms.is_valid()
        if not formset.is_valid() or not validated:
            return self.render_to_response(self.get_context_data(form=form))
        pecas = forms.save(commit=False)
        total = 0.00
        for price in formset.cleaned_data:
            if len(price) > 0:
                total += float(price["subtotal"].replace(",", "."))
        pecas.total = round(total, 2)
        pecas.save()
        formset.instance = pecas
        formset.save()
        return redirect("website_pecas_list")


class PecasDeleteView(generic.DeleteView):
    model = models.Pecas
    success_url = reverse_lazy("website_pecas_list")
    template_name = "website/pecas/pecas_confirm_delete.html"


class ItensPecasDetailView(generic.DetailView):
    model = models.Pecas
    template_name = "website/pecas/itenspecas_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pecas_id = self.kwargs["pk"]
        name_pecas = context["pecas"]
        queryset = models.Itenspecas.objects.filter(pecas=name_pecas)
        context["itenspecas"] = queryset
        context["pecas_id"] = pecas_id
        context["name_pecas"] = name_pecas
        context["total"] = models.Pecas.objects.get(id=pecas_id).total
        return context


# class ItensPecasCRUD(CRUDView):
#     model = models.Itenspecas
#     template_name_base = "ccruds"
#     form_class = forms.PecasForm
#     namespace = None
#     check_perms = True
#     views_available = ["create", "list", "delete", "update"]
#     fields = [
#         "description",
#         "pecas",
#         "price",
#         "quantity",
#         "subtotal",
#     ]
#     list_fields = [
#         "id",
#         "description",
#         "pecas",
#         "price",
#         "quantity",
#         "subtotal",
#     ]
#     add_form = forms.ItensPecasForm
#     update_form = forms.ItensPecasForm
#     paginate_by = 40


# class RabbiitCRUD(CRUDView):
#     model = models.Rabbiit
#     template_name_base = "ccruds"
#     namespace = None
#     check_perms = True
#     views_available = ["create", "list", "delete", "update"]
#     list_fields = [
#         "created_at",
#         "description",
#         "time_start",
#         "time_end",
#         "time_total",
#         "rate_hour",
#         "rate_total",
#     ]
#     search_fields = ["description__icontains"]
#     add_form = forms.RabbiitForm
#     update_form = forms.RabbiitForm


class RabbiitListView(LoginRequiredMixin, generic.TemplateView):
    model = models.Rabbiit
    template_name = "website/rabbiit/rabbiit_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset_list = models.Rabbiit.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(comercio__icontains=query) | Q(data__icontains=query)
            ).distinct()

        paginator = Paginator(queryset_list, 5)  # Show 5 pecas per page
        page = self.request.GET.get("page")
        try:
            queryset_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 999), deliver last page of results.
            queryset_list = paginator.page(paginator.num_pages)

        return queryset_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_pecas = models.Rabbiit.objects.order_by("-id")
        # queryset_list = Pecas.objects.all()
        query = self.request.GET.get("q")
        if query:
            list_pecas = list_pecas.filter(
                Q(comercio__description__icontains=query) | Q(data__icontains=query)
            ).distinct()
        paginator = Paginator(list_pecas, self.paginate_by)

        page = self.request.GET.get("page")

        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        context["object_list"] = object_list
        context["model_verbose_name_plural"] = self.model._meta.verbose_name_plural
        return context


# class RabbiitCreateView(generic.CreateView):
#     model = models.Rabbiit
#     template_name = "website/rabbiit/rabbiit_create.html"
#     form_class = forms.RabbiitForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["forms"] = forms.RabbiitForm(self.request.POST)
#         else:
#             context["forms"] = forms.RabbiitForm()
#         context[
#             "model_verbose_name_plural"
#         ] = self.model._meta.verbose_name_plural
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         forms = context["forms"]
#         if not forms.is_valid():
#             return self.render_to_response(self.get_context_data(form=form))
#         self.object = form.save()
#         forms.instance = self.object
#         forms.save()
#         return redirect("website_rabbiit_list")


# class RabbiitEditView(generic.UpdateView):
#     model = models.Rabbiit
#     template_name = "website/horatrabalhada/horatrabalhada_form.html"
#     form_class = forms.RabbiitForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["forms"] = forms.RabbiitForm(
#                 self.request.POST, instance=self.object
#             )
#         else:
#             context["forms"] = forms.RabbiitForm(instance=self.object)
#         return context

# def form_valid(self, form):
#     context = self.get_context_data()
#     form = context['forms']
#     formset = context['formset']
#     if form.is_valid():
#         sizeIensPecas = len(formset.cleaned_data)
#         try:
#             form.cleaned_data['total'] = str(total)
#         except Exception as err:
#             form.cleaned_data['total'] = 0
#             print(f'Err.: {err}')
#         # form = form.save(commit=False)
#         # form.total = str(total)
#         form.save()
#         formset.save()
#     return redirect('website_horatrabalhada_list')
#     else:
#         return self.render_to_response(self.get_context_data(form=form))


class RabbiitDeleteView(generic.DeleteView):
    success_url = reverse_lazy("website_horatrabalhada_list")
    model = models.Rabbiit
    template_name_suffix = "/horatrabalhada_confirm_delete"


class HoraTrabalhadaListView(generic.TemplateView):
    model = models.HoraTrabalhada
    template_name = "website/horatrabalhada/horatrabalhada_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset_list = models.HoraTrabalhada.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(comercio__icontains=query) | Q(data__icontains=query)
            ).distinct()

        paginator = Paginator(queryset_list, 5)  # Show 5 pecas per page
        page = self.request.GET.get("page")
        try:
            queryset_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 999), deliver last page of results.
            queryset_list = paginator.page(paginator.num_pages)

        return queryset_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_pecas = models.HoraTrabalhada.objects.order_by("-id")
        query = self.request.GET.get("q")
        if query:
            list_pecas = list_pecas.filter(
                Q(comercio__description__icontains=query) | Q(data__icontains=query)
            ).distinct()
        paginator = Paginator(list_pecas, self.paginate_by)

        page = self.request.GET.get("page")

        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        context["object_list"] = object_list
        return context


class HoraTrabalhadaCreateView(generic.CreateView):
    model = models.HoraTrabalhada
    template_name = "website/horatrabalhada/horatrabalhada_form.html"
    form_class = forms.HoraTrabalhadaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = forms.HoraTrabalhadaForm(self.request.POST)
        else:
            context["forms"] = forms.HoraTrabalhadaForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["forms"]
        if not forms.is_valid():
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()
        forms.instance = self.object
        forms.save()
        return redirect("website_horatrabalhada_list")


class HoraTrabalhadaEditView(generic.UpdateView):
    model = models.HoraTrabalhada
    template_name = "website/horatrabalhada/horatrabalhada_form.html"
    form_class = forms.HoraTrabalhadaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = forms.HoraTrabalhadaForm(
                self.request.POST, instance=self.object
            )
        else:
            context["forms"] = forms.HoraTrabalhadaForm(instance=self.object)
        return context


class HoraTrabalhadaDeleteView(generic.DeleteView):
    success_url = reverse_lazy("website_horatrabalhada_list")
    model = models.HoraTrabalhada
    template_name_suffix = "/horatrabalhada_confirm_delete"


# class CityCRUD(LoginRequiredMixin, CRUDView):
#     model = models.City
#     template_name_base = "cruds"
#     check_perms = True
#     views_available = ["create", "list", "delete", "update"]
#     add_form = forms.CityForm
#     update_form = forms.CityForm
#     paginate_by = 40
#     fields = [
#         "id",
#         "description",
#     ]
#     list_fields = [
#         "id",
#         "description",
#     ]
#     search_fields = ["description__icontains"]
#     split_space_search = " "  # default False
#
#     def get_list_view(self):
#         ListViewClass = super().get_list_view()
#
#         class MyListView(ListViewClass):
#             def get_context_data(self):
#                 context = super().get_context_data()
#                 cities = models.City.objects.all()
#                 if (
#                         self.request.GET.get("limpar")
#                         and "q" in self.request.session
#                 ):
#                     del self.request.session["q"]
#                 if search := self.request.GET.get("q"):
#                     self.request.session["q"] = search
#                     RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")
#                     if RE_INT.match(search):
#                         cities = cities.filter(id=search).distinct()
#                         del self.request.session["q"]
#                     else:
#                         cities = cities.filter(
#                             description__icontains=search
#                         ).distinct()
#                 if query := self.request.session.get("q"):
#                     cities = cities.filter(
#                         description__icontains=query
#                     ).distinct()
#                 return context
#
#         return MyListView


class CityListView(generic.ListView):
    model = models.City
    template_name = (
        "website/../localization/templates/localization/localization_list.html"
    )
    context_object_name = "localidades"
    paginate_by = 10

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
                filters |= Q(id=search)
            filters |= Q(description__icontains=search)
        return queryset.filter(filters)


def CitySearchView(request):
    template_name = "website/localization/localization_table.html"
    query = request.POST.get("q")
    cities = models.City.objects.filter(description__icontains=query)
    context = {"object_list": cities}
    return render(request, template_name, context)


class CityCreateView(generic.CreateView):
    model = models.City
    template_name = (
        "website/../localization/templates/localization/localization_form.html"
    )
    form_class = forms.CityForm
    # success_url = "website/localization/localization_result.html"


def form_valid(self, form):
    context = self.get_context_data()
    # form = context["form"]
    # self.object = form.save()
    # form.instance = self.object
    # form.save()
    return render(
        self.request,
        "website/../localization/templates/localization/localization_result.html",
        context,
    )


class CityDetailsView(generic.DetailView):
    model = models.City
    template_name = (
        "website/../localization/templates/localization/localization_detail.html"
    )


class CityEditView(generic.UpdateView):
    model = models.City
    template_name = (
        "website/../localization/templates/localization/localization_update_form.html"
    )
    form_class = forms.CityForm

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["form"]
        self.object = form.save()
        forms.instance = self.object
        forms.save()
        return render(
            self.request,
            "website/../localization/templates/localization/localization_result.html",
            context,
        )


class CityDeleteView(generic.DeleteView):
    model = models.City
    success_url = "/localization"


class ComercioListView(generic.ListView):
    model = models.Comercio
    template_name = "website/comercio/comercio_list.html"
    context_object_name = "comercios"
    paginate_by = 10

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
                filters |= Q(id=search)
            filters |= Q(description__icontains=search)
        return queryset.filter(filters)


# class ComercioCreateView(generic.CreateView):
#     model = models.Comercio
#     template_name = "website/comercio/comercio_create.html"
#     form_class = forms.ComercioForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["form"] = forms.ComercioForm(self.request.POST)
#         else:
#             context["last_data"] = models.Comercio.objects.first()
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         form = context["form"]
#         if not form.is_valid():
#             return self.render_to_response(self.get_context_data(form=form))
#         self.object = form.save()
#         form.instance = self.object
#         form.save()
#         return redirect("website_comercio_list")
#
#
# class ComercioEditView(generic.UpdateView):
#     model = models.Comercio
#     template_name = "website/comercio/comercio_edit.html"
#     form_class = forms.ComercioForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             # context["forms"] = ComercioForm(self.request.POST, instance=self.object)
#             context["form"] = forms.ComercioForm(
#                 self.request.POST, instance=self.object
#             )
#         else:
#             context["form"] = forms.ComercioForm(instance=self.object)
#             # context["forms"] = ComercioForm(instance=self.object)
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         forms = context["form"]
#         if not forms.is_valid():
#             return self.render_to_response(self.get_context_data(form=form))
#         self.object = form.save()
#         forms.instance = self.object
#         forms.save()
#         return redirect("website_comercio_list")


class ComercioDeleteView(generic.DeleteView):
    success_url = reverse_lazy("website_comercio_list")
    model = models.Comercio
    template_name_suffix = "/comercio_confirm_delete"


class AutoResponseView(generic.ListView):
    ...


class EventsListView(LoginRequiredMixin, generic.ListView):
    model = models.Events
    template_name = "website/events/events_list.html"
    paginate_by = 10
    ordering = ["-event_date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()
        return context

    def get_queryset(self):
        # queryset = super(EventsListView, self).get_queryset()
        queryset = models.Events.objects.all()
        filters = Q()
        if search := self.request.GET.get("search"):
            RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")
            # Essa linha qdo quero trazer o ID
            if RE_INT.match(search):
                filters |= Q(id=search)
            filters |= Q(description__icontains=search)
        return queryset.filter(filters).order_by("-event_date")


# class EventsCreateView(generic.CreateView):
#     model = models.Events
#     template_name = "website/events/events_form.html"
#     form_class = forms.EventsForm
#
#
# class EventsEditView(generic.UpdateView):
#     model = models.Events
#     template_name = "website/events/events_form.html"
#     form_class = forms.EventsForm
#
#     def get_success_url(self):
#         return reverse("website_events_list")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["forms"] = forms.EventsForm(
#                 self.request.POST, instance=self.object
#             )
#         else:
#             context["forms"] = forms.EventsForm(instance=self.object)
#         return context


class EventsDeleteView(generic.DeleteView):
    model = models.Events
    success_url = reverse_lazy("website_events_list")
    template_name = "website/events/events_confirm_delete.html"


class VivoListView(LoginRequiredMixin, generic.ListView):
    model = models.Vivo
    template_name = "website/vivo/vivo_list.html"
    paginate_by = 10

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
                filters |= Q(id=search)
            filters |= Q(company__name__icontains=search)
        return queryset.filter(filters)


# class VivoCreateView(generic.FormView):
#     model = models.Vivo
#     template_name = "website/vivo/vivo_form.html"
#     form_class = forms.VivoForm
#     success_url = "website/vivo/vivo_detail.html"
#
#     def post(self, request, *args, **kwargs):
#         success_url = reverse("vivo-detail")
#         return HttpResponseRedirect(success_url)
#
#
# def model_form_upload(request):
#     if request.method == "POST":
#         form = forms.VivoForms(request.POST, request.FILES)
#         results = form.files["file"].file.getvalue().decode("utf-8").split("\r")
#         # Consumido..: 1.52 GB em %..: 50.83%
#         # Disponivel..: 1.48 GB em %..: 49.17%
#         "internet_used_in_percentagem = 50.83%"
#         "internet_used_in_number = 1.52 GB"
#         "internet_available_in_percentagem = 49.17%"
#         "internet_available_in_number = 1.48 GB"
#
#         # 642.57 MB 02/11/21 - 11h01 R$ 0,00
#         "velocity = 642.57 MB"
#         "event_date = 02/11/21"
#         "time = 11h01"
#         "price = R$ 0,00"
#
#         return render(
#             request, "website/vivo/model_form_upload.html", {"results": results}
#         )
#     form = forms.VivoForms()
#     return render(
#         request, "website/vivo/model_form_upload.html", {"form": form}
#     )
#
#
# class VivoEditView(generic.UpdateView):
#     model = models.Vivo
#     template_name = "website/vivo/vivo_form.html"
#     form_class = forms.VivoForm
#
#     def get_success_url(self):
#         return reverse("website_vivo_list")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["forms"] = forms.VivoForm(
#                 self.request.POST, instance=self.object
#             )
#         else:
#             context["forms"] = forms.VivoForm(instance=self.object)
#         return context


class VivoDeleteView(generic.DeleteView):
    model = models.Vivo
    success_url = reverse_lazy("website_vivo_list")
    template_name = "website/vivo/vivo_confirm_delete.html"


class AutoCompleteView(generic.FormView):
    def get(self, request):
        if q := self.request.GET.get("term", "").capitalize():
            events = (
                models.Events.objects.filter(description__icontains=q)
                .values("description")
                .order_by("description")
                .distinct()
            )
            data = list(events)
            return JsonResponse(data, safe=False)
        return JsonResponse({})

    def page2dict(self, events):
        return {
            "events": [a.to_dict() for a in events],
        }


class PlanilhaListView(LoginRequiredMixin, generic.TemplateView):
    model = models.Planilha
    template_name = "website/planilha/planilha_list.html"


class EmpregoListView(LoginRequiredMixin, generic.ListView):
    model = models.Emprego
    template_name = "website/emprego/emprego_list.html"
    paginate_by = 10
    ordering = ["-entrade_date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count_feedback"] = (
            self.get_queryset().filter(feedback__isnull=True).count()
        )
        context["count_non_feedback"] = (
            self.get_queryset().filter(feedback__isnull=False).count()
        )
        context["count_geral"] = self.get_queryset().count()
        columns = [
            "ID",
            "Data do contato",
            "Empresa",
            "Vaga",
            "Data do feedback",
            "Dias passados",
        ]
        styles = ["", "", "", "", "", "text-align: center"]
        context["columns_styles"] = zip(columns, styles)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()
        if search := self.request.GET.get("search"):
            RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")
            # Essa linha qdo quero trazer o ID
            if RE_INT.match(search):
                filters |= Q(id=search)
            filters |= Q(job__icontains=search)
            filters |= Q(company__name__icontains=search)
            queryset = queryset.filter(filters)
        if self.request.GET.get("is_feedback"):
            filters |= Q(feedback__isnull=False)
        return queryset.filter(filters)


# class EmpregoCreateView(generic.CreateView):
#     model = models.Emprego
#     template_name = "website/emprego/emprego_form.html"
#     form_class = forms.EmpregoForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["forms"] = forms.EmpregoForm(self.request.POST)
#         else:
#             context["forms"] = forms.EmpregoForm()
#             context["create_or_edit"] = "CADASTRAR"
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         form = context["form"]
#         if not form.is_valid():
#             return self.render_to_response(self.get_context_data(form=form))
#         emprego = form.save(commit=False)
#         try:
#             emprego.count_day_contact = \
#                 (form.instance.feedback_date - form.instance.entrade_date).days
#         except TypeError:
#             pass
#         emprego.save()
#         empresa = models.Empresa.objects.get(id=form.instance.company.id)
#         empresa.amount_applied += 1
#         empresa.save()
#         form.save_m2m()
#         return redirect("website_emprego_list")
#
#
# class EmpregoEditView(generic.UpdateView):
#     model = models.Emprego
#     template_name = "website/emprego/emprego_form.html"
#     form_class = forms.EmpregoForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["forms"] = forms.EmpregoForm(
#                 self.request.POST, instance=self.object
#             )
#         else:
#             context["forms"] = forms.EmpregoForm(instance=self.object)
#             context["create_or_edit"] = "EDITAR"
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         form = context["form"]
#         if not form.is_valid():
#             return self.render_to_response(self.get_context_data(form=form))
#         emprego = form.save(commit=False)
#         if int(form.data["count_day_contact"]) < 1:
#             try:
#                 emprego.count_day_contact = \
#                     (form.instance.feedback_date - form.instance.entrade_date).days
#             except TypeError:
#                 pass
#         emprego.save()
#         form.save_m2m()
#         return redirect("website_emprego_list")


class EmpregoDetailView(generic.DetailView):
    model = models.Emprego
    template_name = "website/emprego/emprego_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["skills"] = models.Skill.objects.filter(
            emprego__id=context["object"].id
        )
        context["vacancy_found"] = [
            item[1]
            for item in constants.TYPE_VACANCY_FOUND
            if context["object"].vacancy_found in item[0]
        ][0]
        context["process_fase"] = [
            item[1]
            for item in constants.TYPE_PROCCESS_FASE
            if context["object"].process_fase in item[0]
        ][0]
        return context


class EmpregoDeleteView(generic.DeleteView):
    model = models.Emprego
    success_url = reverse_lazy("website_emprego_list")
    template_name = "website/emprego/emprego_confirm_delete.html"


class SkillsListView(LoginRequiredMixin, generic.ListView):
    model = models.Skill
    template_name = "website/emprego/skills_list.html"
    paginate_by = 10

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
                filters |= Q(id=search)
            filters |= Q(description__icontains=search)
        return queryset.filter(filters)


# class SkillsCreateView(generic.CreateView):
#     model = models.Skill
#     template_name = "website/emprego/skills_form.html"
#     form_class = forms.SkillsForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["forms"] = forms.SkillsForm(self.request.POST)
#         else:
#             context["forms"] = forms.SkillsForm()
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         forms = context["forms"]
#         if not forms.is_valid():
#             return self.render_to_response(self.get_context_data(form=form))
#         self.object = form.save()
#         forms.instance = self.object
#         forms.save()
#         return redirect("website_skills_list")
#
#
# class SkillsEditView(generic.UpdateView):
#     model = models.Skill
#     template_name = "website/emprego/skills_form.html"
#     form_class = forms.SkillsForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["forms"] = forms.SkillsForm(
#                 self.request.POST, instance=self.object
#             )
#         else:
#             context["forms"] = forms.SkillsForm(instance=self.object)
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         forms = context["form"]
#         if not forms.is_valid():
#             return self.render_to_response(self.get_context_data(form=form))
#         self.object = form.save()
#         forms.instance = self.object
#         forms.save()
#         return redirect("website_skills_list")


class SkillsDeleteView(generic.DeleteView):
    model = models.Skill
    success_url = reverse_lazy("website_skills_list")
    template_name = "website/emprego/skills_confirm_delete.html"


class EmpresaListView(LoginRequiredMixin, generic.ListView):
    model = models.Empresa
    template_name = "website/emprego/empresa_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()
        columns = ["ID", "Nome", "Site", "Qt aplicada", "Cultura", "Ações"]
        styles = [
            "",
            "",
            "",
            "text-align: center",
            "text-align: center",
            "text-align: center",
        ]
        list_empresa = []
        for empresa in context["empresa_list"]:
            site = "" if len(empresa.site) < 8 else empresa.site
            dict_empresa = {
                "id": empresa.id,
                "name": empresa.name,
                "site": site,
                "amount_applied": empresa.amount_applied,
                "company_culture": empresa.company_culture,
            }
            list_empresa.append(dict_empresa)
        context["columns_styles"] = zip(columns, styles)
        context["empresa_list"] = list_empresa
        # context["site"] = empresa.site if len(empresa.site) > 7 else ''
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()
        if search := self.request.GET.get("search"):
            RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")
            # Essa linha qdo quero trazer o ID
            if RE_INT.match(search):
                filters |= Q(id=search)
            filters |= Q(name__icontains=search)
        return queryset.filter(filters)


# class EmpresaCreateView(generic.CreateView):
#     model = models.Empresa
#     template_name = "website/emprego/empresa_form.html"
#     form_class = forms.EmpresaForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["forms"] = forms.EmpresaForm(self.request.POST)
#         else:
#             context["forms"] = forms.EmpresaForm()
#             context["create_or_edit"] = "CADASTRAR"
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         forms = context["forms"]
#         if not forms.is_valid():
#             return self.render_to_response(self.get_context_data(form=form))
#         self.object = form.save()
#         forms.instance = self.object
#         forms.save()
#         if forms.cleaned_data["consulting"]:
#             consultancy = models.Consultancy.objects.get(
#                 name=forms.cleaned_data["consulting"]
#             )
#             consultancy.quantity_of_company += 1
#             consultancy.save()
#         return redirect("website_empresa_list")
#
#
# class EmpresaEditView(generic.UpdateView):
#     model = models.Empresa
#     template_name = "website/emprego/empresa_form.html"
#     form_class = forms.EmpresaForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["forms"] = forms.EmpresaForm(
#                 self.request.POST, instance=self.object
#             )
#         else:
#             context["forms"] = forms.EmpresaForm(instance=self.object)
#             context["create_or_edit"] = "EDITAR"
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         forms = context["form"]
#         if not forms.is_valid():
#             return self.render_to_response(self.get_context_data(form=form))
#         self.object = form.save()
#         forms.instance = self.object
#         forms.save()
#         return redirect("website_empresa_list")


class EmpresaDetailView(generic.DetailView):
    model = models.Empresa
    template_name = "website/emprego/empresa_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa = models.Empresa.objects.get(id=self.kwargs["pk"])
        context["site"] = empresa.site if len(empresa.site) > 7 else ""
        return context


class EmpresaDeleteView(generic.DeleteView):
    model = models.Empresa
    success_url = reverse_lazy("website_empresa_list")
    template_name = "website/emprego/empresa_confirm_delete.html"


class ConsultancyListView(LoginRequiredMixin, generic.ListView):
    model = models.Consultancy
    template_name = "website/emprego/consultancy_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()
        columns = [
            "ID",
            "Nome",
            "Qt Empresas",
        ]
        styles = ["", "", "", "text-align: center"]
        context["columns_styles"] = zip(columns, styles)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()
        if search := self.request.GET.get("search"):
            RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")
            # Essa linha qdo quero trazer o ID
            if RE_INT.match(search):
                filters |= Q(id=search)
            filters |= Q(name__icontains=search)
        return queryset.filter(filters)


# class ConsultancyCreateView(generic.CreateView):
#     model = models.Consultancy
#     template_name = "website/emprego/consultancy_form.html"
#     form_class = forms.ConsultancyForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["forms"] = forms.ConsultancyForm(self.request.POST)
#         else:
#             context["forms"] = forms.ConsultancyForm()
#             context["create_or_edit"] = "CADASTRAR"
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         forms = context["forms"]
#         if not forms.is_valid():
#             return self.render_to_response(self.get_context_data(form=form))
#         self.object = form.save()
#         forms.instance = self.object
#         forms.save()
#         return redirect("website_consultancy_list")
#
#
# class ConsultancyEditView(generic.UpdateView):
#     model = models.Consultancy
#     template_name = "website/emprego/consultancy_form.html"
#     form_class = forms.ConsultancyForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["forms"] = forms.ConsultancyForm(
#                 self.request.POST, instance=self.object
#             )
#         else:
#             context["forms"] = forms.ConsultancyForm(instance=self.object)
#             context["create_or_edit"] = "EDITAR"
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         forms = context["form"]
#         if not forms.is_valid():
#             return self.render_to_response(self.get_context_data(form=form))
#         self.object = form.save()
#         forms.instance = self.object
#         forms.save()
#         return redirect("website_consultancy_list")


class ConsultancyDeleteView(generic.DeleteView):
    model = models.Consultancy
    success_url = reverse_lazy("website_consultancy_list")
    template_name = "website/emprego/consultancy_confirm_delete.html"


# def import_comercio(request):
#     template_name = "website/comercio/import.html"
#     if request.method == "POST":
#         comercio_resource = ComercioResource()
#         dataset = tablib.Dataset()
#         new_comercio = request.FILES["arquivo"]
#         imported_data = dataset.load(
#             new_comercio.read().decode("utf-8"), format="tsv"
#         )
#         result = comercio_resource.import_data(
#             imported_data, dry_run=True, collect_failed_rows=True
#         )  # Test the data import
#         if not result.has_errors():
#             comercio_resource.import_data(
#                 imported_data, dry_run=False
#             )  # Actually import now
#         context = {
#             "result": result,
#         }
#     else:
#         context = {}
#     return render(request, template_name, context)


# def import_pecas(request):
#     template_name = "website/pecas/import.html"
#     pecas_resource = PecasResource()
#     from_encoding = "utf-8"
#
#     form = forms.ImportForm(
#         import_formats, request.POST or None, request.FILES or None
#     )
#
#     if request.method == "POST" and form.is_valid():
#         input_format = import_formats[int(form.cleaned_data["input_format"])]()
#         import_file = form.cleaned_data["import_file"]
#         # first always write the uploaded file to disk as it may be a
#         # memory file or else based on settings upload handlers
#         with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
#             for chunk in import_file.chunks():
#                 uploaded_file.write(chunk)
#         # then read the file, using the proper format-specific mode
#         with open(
#                 uploaded_file.name, input_format.get_read_mode()
#         ) as uploaded_import_file:
#             # warning, big files may exceed memory
#             data = uploaded_import_file.read()
#             if not input_format.is_binary() and from_encoding:
#                 data = force_text(data, from_encoding)
#             dataset = input_format.create_dataset(data)
#             result = pecas_resource.import_data(
#                 dataset,
#                 dry_run=True,
#                 raise_errors=False,
#             )
#         context = {}
#         if not result.has_errors() and not result.has_validation_errors():
#             context["confirm_form"] = ConfirmImportForm(
#                 initial={
#                     "import_file_name": os.path.basename(uploaded_file.name),
#                     "input_format": form.cleaned_data["input_format"],
#                     "original_file_name": uploaded_file.name,
#                 }
#             )
#         context["form"] = form
#         context["result"] = result
#         context["fields"] = list(pecas_resource.fields)
#         return render(request, template_name, context)
#     else:
#         context = {"fields": list(pecas_resource.fields), "form": form}
#         return render(request, template_name, context)


# def pecas_import_pecas(request):
#     pecas_resource = PecasResource()
#     if request.method == "POST":
#         input_format = import_formats[int(request.POST["input_format"])]()
#         with open(request.POST["original_file_name"]) as uploaded_import_file:
#             # warning, big files may exceed memory
#             data = uploaded_import_file.read()
#             dataset = input_format.create_dataset(data)
#             pecas_resource.import_data(dataset)
#         os.remove(uploaded_import_file.name)
#     return redirect("website_pecas_import")


# class ChatgptListView(LoginRequiredMixin, generic.TemplateView):
#     template_name = "website/chatgpt/chatgpt_list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['respostas'] = 'Não foi feita perguntas ao chatGPT'
#         pergunta = self.request.GET.get('pergunta')
#         if pergunta:
#             try:
#                 resposta = chatgpt.main(pergunta)
#                 context['respostas'] = resposta
#             except Exception:
#                 context['respostas'] = 'Excedeu a capacidade de perguntas'
#             context['pergunta'] = pergunta
#         return context
