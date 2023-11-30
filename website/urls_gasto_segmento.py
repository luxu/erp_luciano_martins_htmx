from django.urls import include, path

from . import views_gasto_segmento as views


segmento_view = views.SegmentoCRUD()

urlpatterns = [
    path(
        "gasto/",
        views.GastosListView.as_view(),
        name="website_gasto_list",
    ),
    path(
        "website/gasto/create/",
        views.GastosCreateView.as_view(),
        name="website_gasto_create",
    ),
    path(
        "website/gasto/<int:pk>/edit/",
        views.GastosEditView.as_view(),
        name="website_gasto_edit",
    ),
    path(
        "website/gasto/<int:pk>/delete/",
        views.GastosDeleteView.as_view(),
        name="website_gasto_delete",
    ),
    path("gastosPorMes/", views.GastosPorMesView, name="gastosPorMes"),
    path(
        "gastosPorSegmento/",
        views.GastoPorSegmentoView,
        name="gastosPorSegmento",
    ),
    path(
        "gastosPorParcelas/",
        views.GastoPorParcelasView,
        name="gastosPorParcelas",
    ),
    path(
        "gasto/autocomplete/",
        views.AutoCompleteView.as_view(),
        name="website_gastos_autocomplete",
    ),
    path("", include(segmento_view.get_urls())),
    path(
        "detailsSegmento/<str:segmento_name>/",
        views.DetailsSegmentoView,
        name="detailsSegmento",
    ),
    path(
        "subdividirSegmentos/",
        views.SubdividirSegmentosView,
        name="subdividirSegmentos",
    ),
]
