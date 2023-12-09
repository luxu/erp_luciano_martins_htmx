from django.forms import ModelForm

from .models import Gasto, Segmento


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


class GastoFormAdmin(ModelForm):
    def __init__(self, *args, **kwargs):
        super(GastoFormAdmin, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'mask-name'

class SegmentoForm(ModelForm):
    class Meta:
        model = Segmento
        fields = [
            "name",
        ]