import re

import fitz
from decouple import config
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)
from pyitau import Itau

from .forms import GastoForm
from .models import Gasto


class GastoListView(ListView):
    model = Gasto
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()
        return context


def GastoSearchView(request):
    template_name = "gasto/gasto_table.html"
    query = request.POST.get("q")
    cities = Gasto.objects.filter(description__icontains=query)
    context = {"object_list": cities}
    return render(request, template_name, context)


class GastoCreateView(CreateView):
    model = Gasto
    template_name = "localization/localization_form.html"
    form_class = GastoForm
    # success_url = "website/localization/localization_result.html"


def form_valid(self, form):
    context = self.get_context_data()
    return render(self.request, "localization/localization_result.html", context)


class GastoDetailsView(DetailView):
    model = Gasto
    # template_name = "localization/gasto_detail.html"


class GastoEditView(UpdateView):
    model = Gasto
    form_class = GastoForm

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     forms = context["form"]
    #     self.object = form.save()
    #     forms.instance = self.object
    #     forms.save()
    #     return render(self.request, "localization/localization_result.html", context)


class GastoDeleteView(DeleteView):
    model = Gasto
    success_url = "/gasto"


class AutoCompleteView(FormView):
    def get(self, request):
        if q := request.GET.get("term").capitalize():
            gastos = (
                Gasto.objects.filter(name__icontains=q)
                .values("name")
                .order_by("name")
                .distinct()
            )
            results = ",".join([str(gasto["name"]) for gasto in gastos])
            return HttpResponse(results)


def read_pdf(request):
    template_name = "gasto/pdf.html"
    if request.method == "POST":
        pdf_file = request.FILES["pdf_file"]
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        texto = ""
        for pagina in pdf_document:
            texto += pagina.get_text()
        tabelas = texto.split("Data")[1:]
        padrao = r"\b\d{2}/\d{2}\b"
        cont = 1
        table_lancamentos = None
        lista_contas_parceladas = []
        context = {}
        list_line = []
        for page in tabelas:
            texts = page.split("\n")
            line = ""
            for text in texts:
                if "Lançamentos em processamento" in text:
                    table_lancamentos = tabelas[-1]
                    break
                else:
                    if re.search(padrao, text):
                        line = text
                    if "," in text:
                        line += text
                        if "PARC" in line:
                            lista_contas_parceladas.append(line)
                        else:
                            if re.search(padrao, line):
                                list_line.append(line)
                                cont += 1
                                line = ""
            if table_lancamentos:
                break
        context["list_line"] = list_line
        if lista_contas_parceladas:
            list_parcela = []
            for parcela in lista_contas_parceladas:
                list_parcela.append(parcela)
            context["lista_contas_parceladas"] = list_parcela
        if table_lancamentos:
            texts = table_lancamentos.split("\n")
            line = ""
            for text in texts[3:]:
                if re.search(padrao, text):
                    line = text
                else:
                    line += text
                if "," in text:
                    line = ""
        return render(request, template_name, context)
    return render(request, template_name)


def record_pdf(request):
    template_name = "gasto/record_pdf.html"
    dados_selecionados = request.POST.getlist("selecionar")
    lista_dados = []
    for item in dados_selecionados:
        dados = item.strip().split(" ")
        data = dados[0]
        estabelecimento = " ".join(dados[1:-2])
        # gasto = Gasto.objects.filter(name__icontains=estabelecimento)
        for info in estabelecimento.split(" "):
            gasto = Gasto.objects.filter(name__icontains=info)
            if gasto:
                estabelecimento = gasto.first().name
                break
        preco = dados[-1]
        dict_dados = {"data": data, "estabelecimento": estabelecimento, "preco": preco}
        lista_dados.append(dict_dados)
    context = {"lista_dados": lista_dados}
    return render(request, template_name, context)


def access_itau(request):
    template_name = 'gasto/result_itau.html'
    dados_itau = internetbaking()
    # dados_itau = {
    #     "01/01/2023": {"descricao": "Compra", "preco": 100.0},
    #     "02/01/2023": {"descricao": "Venda", "preco": 150.0},
    # }
    context = {
        "dados_itau": dados_itau,
    }
    """
    DATA..:2023-12-23
    DESCRIÇÃO..Drogasil    -ct
    VALOR..40,19
    27
    """
    return render(request, template_name, context)


def internetbaking():
    itau = Itau(
        agency="4533",
        account="27693",
        account_digit="9",
        password=config("ITAU_PASSWORD"),
    )
    itau.authenticate()
    # fatura_passada = itau.get_credit_card_invoice()["object"]["faturas"][0][
    #     "lancamentosNacionais"
    # ]["titularidades"][0]["lancamentos"]
    fatura_atual = itau.get_credit_card_invoice()["object"]["faturas"][1][
        "lancamentosNacionais"
    ]["titularidades"][0]["lancamentos"]
    line = "-" * 80
    list_infos = {}
    for item in fatura_atual:
        # for index, item in enumerate(fatura_passada):
        data = item["data"]
        descricao = item["descricao"]
        valor = item["valor"]
        list_infos = {
            'data': data,
            'info': {
                'descricao': descricao,
                'valor': valor
            }
    }
    print(
        f"{line}\nDATA..:{data}\nDESCRIÇÃO..{descricao}\nVALOR..{valor}"
    )
    return list_infos


def read_itau_txt(request):
    template_name = "gasto/itau_txt.html"
    fatura_passada = []
    fatura_atual = []
    if request.method == "POST":
        itau_file = request.FILES["itau_file"]
        resultado = itau_file.read().decode("utf-8").split("\n")
        for info in resultado:
            print(info)
        context = {"fatura_passada": fatura_passada, "fatura_atual": fatura_atual}
        return render(request, template_name, context)

    return render(request, template_name)
