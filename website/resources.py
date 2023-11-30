# from import_export import resources

from website.models import Comercio, Pecas


# class ComercioResource(resources.ModelResource):
#     class Meta:
#         model = Comercio
#         exclude = ("status",)
#
#
# class PecasResource(resources.ModelResource):
#     class Meta:
#         model = Pecas
#         fields = [
#             "id",
#             "data",
#             "veiculo",
#             "proxtroca",
#             "troca",
#             "comercio",
#             "city",
#             "total",
#         ]
