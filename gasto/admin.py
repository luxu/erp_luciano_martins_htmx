from django.contrib import admin

from .forms import GastoFormAdmin, SegmentoForm
from .models import Gasto, Parcelas, Segmento


class ParcelasInline(admin.TabularInline):
    model = Parcelas
    extra = 1


@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    inlines = (ParcelasInline,)
    list_display = (
        "id",
        "name",
        "datagasto",
        "soma",
        "segmento",
    )
    readonly_fields = ("soma",)
    search_fields = ("name",)
    form = GastoFormAdmin
    fieldsets = (
        (
            "Info",
            {
                "classes": ("extrapretty",),
                "fields": [
                    ("name", "more_infos"),
                    ("description_on_invoice", "datagasto"),
                    ("opcoes_cartao", "card_bank"),
                    ("segmento"),
                ],
            },
        ),
    )

    class Media:
        css = {
            "all": ["https://code.jquery.com/ui/1.13.2/themes/base/jquery-ui.css"],
        }
        js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js",
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.13.2/jquery-ui.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js",
            "main.js",
        )


@admin.register(Parcelas)
class ParcelasAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "gasto",
        "parcelas",
        "numero_parcela",
        "valor_parcela",
        "data_parcela",
    )
    list_filter = ("numero_parcela",)


@admin.register(Segmento)
class SegmentoAdmin(admin.ModelAdmin):
    form = SegmentoForm
    list_display = (
        "id",
        "name",
    )
