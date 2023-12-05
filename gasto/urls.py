from django.urls import path

from . import views

urlpatterns = [
    path("", views.GastoListView.as_view(), name="gasto_list"),
    path("search/", views.GastoSearchView, name="gasto_search"),
    path("create/", views.GastoCreateView.as_view(), name="gasto_create"),
    path("<int:pk>/", views.GastoDetailsView.as_view(), name='gasto_detail'),
    path("<int:pk>/edit/", views.GastoEditView.as_view(), name="gasto_update"),
    path("<int:pk>/delete/", views.GastoDeleteView.as_view(), name="gasto_delete"),
    path("autocomplete/", views.AutoCompleteView.as_view(), name="website_gastos_autocomplete"),
]
