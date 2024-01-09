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
    # template_name = "localization/localization_form.html"
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


def extrair_texto_do_pdf(pdf_file):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    return "".join(page.get_text() for page in pdf_document)


def read_pdf(request):
    template_name = "gasto/pdf.html"
    context = {}

    if request.method == "POST":
        pdf_file = request.FILES.get("pdf_file")
        if pdf_file:
            texto = extrair_texto_do_pdf(pdf_file)
            tabelas = dividir_texto_em_tabelas(texto)
            dados = processar_tabelas(tabelas)

            context["dados"] = dados

    return render(request, template_name, context)


def dividir_texto_em_tabelas(context, texto):
    # tabelas = texto.split("Data")[1:]
    return texto.split("Data")[1:]


def processar_tabelas(tabelas):
    padrao = r"\b\d{2}/\d{2}\b"
    table_lancamentos = None
    lista_contas_parceladas = []
    list_line = []
    context = {}
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
                            line = ""
        if table_lancamentos:
            break
    context["list_line"] = list_line
    # if lista_contas_parceladas:
    #     context["lista_contas_parceladas"] = lista_contas_parceladas
    # if table_lancamentos:
    #     texts = table_lancamentos.split("\n")
    #     line = ""
    #     for text in texts[3:]:
    #         if re.search(padrao, text):
    #             line = text
    #         else:
    #             line += text
    #         if "," in text:
    #             line = ""
    return context


def expenses_pdf(request):
    """Despesas que foram escolhidas do PDF do BB a serem inseridas no banco de dados"""
    template_name = "gasto/expenses_pdf.html"
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
    template_name = "gasto/result_itau.html"
    # lista = internetbaking()
    # dados_itau = {
    #     "01/01/2023": {"descricao": "Compra", "valor": 100.0},
    #     "02/01/2023": {"descricao": "Venda", "valor": 150.0},
    # }

    # dados_itau = {
    #     'data': '2023-12-23',
    #     'info': {
    #         'descricao': 'Drogasil    -ct',
    #          'valor': '40,19'
    #     }
    # }

    # dados_itau = {
    #     '2023-12-23': {
    #         'descricao': 'Drogasil    -ct',
    #          'valor': '40,19'
    #     }
    # }
    lista = [
        {"2023-12-01": {"descricao": "Sesc Pres Prudente", "valor": "38,00"}},
        {"2023-12-01": {"descricao": "Supermerc Nagai Pp", "valor": "16,75"}},
        {"2023-12-01": {"descricao": "Dm          *tvexpress", "valor": "25,90"}},
    ]

    dados_itau = {}

    # Iterando pela lista e adicionando os valores ao dicionário
    for item in lista:
        for chave, valor in item.items():
            data = chave  # Obtendo a chave (data)
            desc = valor["descricao"]  # Obtendo a descrição
            valor_desc = valor["valor"]  # Obtendo o valor

            if data in dados_itau:
                # Verificando o número de entradas existentes para a data e adicionando o próximo número
                count = len([k for k in dados_itau.keys() if k.startswith(data)])
                # count = len(dados_itau[data])
                nova_chave = f"{data}-{count + 1}"
                dados_itau[nova_chave] = {"descricao": desc, "valor": valor_desc}
            else:
                dados_itau[data] = {"descricao": desc, "valor": valor_desc}

    context = {
        "dados_itau": dados_itau,
    }
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

    list_infos = []
    for item in fatura_atual:
        # for item in fatura_passada:
        data = item["data"]
        descricao = item["descricao"]
        valor = item["valor"]
        dict_infos = {str(data): {"descricao": descricao, "valor": valor}}
        list_infos.append(dict_infos)
    return list_infos


def read_itau_txt(request):
    template_name = "gasto/itau_txt.html"
    # fatura_passada = []
    # fatura_atual = []
    if request.method == "POST":
        itau_file = request.FILES["itau_file"]
        resultado = itau_file.read().decode("utf-8").split("\n")
        for info in resultado:
            print(info)
        # context = {"fatura_passada": fatura_passada, "fatura_atual": fatura_atual}
        context = {"fatura_atual": resultado}
        return render(request, template_name, context)

    return render(request, template_name)
