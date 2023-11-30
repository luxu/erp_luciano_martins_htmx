from django.contrib import admin

# from daterange_filter.filter import DateRangeFilter
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin

from . import models
from .forms import PecasForm
from .forms_gasto_segmento import GastoForm
from .models_gasto_segmento import Gasto, Parcelas, Segmento


class ItensPecasInline(admin.TabularInline):
    model = models.Itenspecas
    extra = 0


# class PecasResource(resources.ModelResource):
#     class Meta:
#         model = models.Pecas
#         exclude = [
#             "status",
#             "created_at",
#             "modified_at",
#         ]


# class PecasAdmin(ImportExportModelAdmin):
#     resource_class = PecasResource
#     form = PecasForm
#     fieldsets = (
#         (
#             None,
#             {
#                 "fields": (
#                     "data",
#                     "veiculo",
#                     "proxtroca",
#                     "troca",
#                     "comercio",
#                     "city",
#                     "total",
#                 )
#             },
#         ),
#     )
#     inlines = (ItensPecasInline,)
#     list_filter = (
#         "data",
#         "veiculo",
#         "comercio",
#         "city",
#     )
#     list_display = (
#         "data",
#         "veiculo",
#         "proxtroca",
#         "troca",
#         "comercio",
#         "city",
#         "total",
#     )
#     ordering = ["-id"]
#
#
# admin.site.register(models.Pecas, PecasAdmin)


class ParcelasInline(admin.TabularInline):
    model = Parcelas
    extra = 1
    fields = ["data_parcela", "parcelas", "numero_parcela", "valor_parcela"]


@admin.register(Gasto)
class GastosAdmin(admin.ModelAdmin):
    # add_form_template = "website/gasto/admin/add_gasto.html"
    form = GastoForm
    list_display = (
        "id",
        "datagasto",
        "name",
        "total",
    )
    # list_filter = (
    #     ("datagasto", DateRangeFilter),
    #     "name",
    # )
    search_fields = ("name",)
    inlines = (ParcelasInline,)
    ordering = ["-id"]


@admin.register(Segmento)
class SegmentoAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Vivo)
class VivoAdmin(admin.ModelAdmin):
    ...


# class ComercioResource(resources.ModelResource):
#     class Meta:
#         model = models.Comercio
#         exclude = [
#             "status",
#             "created_at",
#             "modified_at",
#         ]
#
#
# class ComercioAdmin(ImportExportModelAdmin):
#     resource_class = ComercioResource
#
#
# admin.site.register(models.Comercio, ComercioAdmin)


@admin.register(models.Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "site", "amount_applied"]


class SkillsInline(admin.TabularInline):
    model = models.Skill


@admin.register(models.Emprego)
class EmpregoAdmin(admin.ModelAdmin):
    ordering = ["-entrade_date"]
    list_display = (
        "__str__",
        "company",
        "entrade_date",
        "job",
        "feedback_date",
        "id",
    )
    list_filter = ["feedback_date", "company"]
    date_hierarchy = "entrade_date"
    search_fields = (
        "job",
        "company__name",
    )
    # inlines = [SkillsInline]
    # fieldsets = (
    #     (
    #         None,
    #         {
    #             "fields": (
    #                 ("company", "entrade_date"),
    #                 "job",
    #                 ("process_fase", "vacancy_found", "count_day_contact"),
    #             )
    #         },
    #     ),
    #     (
    #         "Retorno",
    #         {
    #             "fields": (
    #                 "feedback",
    #                 "feedback_date",
    #             )
    #         },
    #     ),
    # )


@admin.register(models.Consultancy)
class ConsultancyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "quantity_of_company")


@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    ...
