from django.forms import ModelForm

from .models import Gasto


class GastoForm(ModelForm):
    class Meta:
        model = Gasto
        fields = [
            "name",
            "more_infos",
            "datagasto",
            "total",
            "description_on_invoice",
            "opcoes_cartao",
            "segmento",
            "card_bank",
        ]
