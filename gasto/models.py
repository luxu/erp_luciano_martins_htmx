from django.db import models

from accounts import constants
from accounts.models import Base

class Segmento(Base):
    name = models.CharField("Tipo de comércio", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Segmento do Comercio"
        verbose_name_plural = "Segmentos do Comercio"
        ordering = ["-name"]
        # db_table = 'website_segmento'



class Cardbank(Base):
    name = models.CharField("Nome", max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Banco do cartão"
        verbose_name_plural = "Bancos do cartão"
        ordering = ["-id"]
        # db_table = 'website_cardbank'


def cardbank_default():
    return Cardbank.objects.get(id=1).id

class Gasto(Base):
    name = models.CharField("nome", max_length=100)
    more_infos = models.CharField(
        "Infos Complementares",
        max_length=100,
        null=True,
        blank=True,
    )
    datagasto = models.DateField("Data do Gasto")
    total = models.CharField(
        "Valor Total", max_length=100, null=True, blank=True
    )
    description_on_invoice = models.CharField(
        "Descrição na fatura", max_length=20, null=True, blank=True
    )
    opcoes_cartao = models.CharField(
        "Tipo de pagamento",
        max_length=1,
        choices=constants.CARTAO,
        default=constants.CREDITO,
    )
    segmento = models.ForeignKey(
        Segmento, related_name="segmento", on_delete=models.PROTECT
    )
    card_bank = models.ForeignKey(
        Cardbank,
        verbose_name="Banco do cartão",
        related_name="cardbanks",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f'{self.id}-{self.name}'

    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
        ordering = ["-id"]
        # db_table = 'website_gasto'


class Parcelas(models.Model):
    gasto = models.ForeignKey(
        Gasto, related_name="parcelas_gasto", on_delete=models.CASCADE
    )
    parcelas = models.IntegerField("Total de parcelas", default=1)
    numero_parcela = models.IntegerField("Número da parcela", default=1)
    valor_parcela = models.CharField(
        "Valor da Parcela", max_length=100, blank=True, null=True
    )
    data_parcela = models.DateField("Installment Date", blank=True, null=True)

    class Meta:
        verbose_name = "Parcela do gasto"
        verbose_name_plural = "Parcelas dos gasto"
        # db_table = 'website_parcelas'

    def __str__(self):
        return f'SEGMENTO..:{self.gasto.name} - PARCELA..:{self.parcelas}'
