from django.contrib import admin
from .models import Gasto, Parcelas

class ParcelasInline(admin.TabularInline):
    model = Parcelas
    extra = 0


@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    inlines = (ParcelasInline,)
    list_display = (
        'id',
        '__str__',
        'datagasto',
        'total',
        'opcoes_cartao',
        'segmento',
        'card_bank',
    )
    search_fields = ('id',)

@admin.register(Parcelas)
class ParcelasAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'gasto',
        'parcelas',
        'numero_parcela',
        'valor_parcela',
        'data_parcela',
    )
    list_filter = ('numero_parcela',)
