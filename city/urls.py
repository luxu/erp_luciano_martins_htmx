from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.CityListView.as_view(),
        name="city_list",
    ),
    path(
        "search/",
        views.CitySearchView,
        name="city_search",
    ),
    path(
        "create/",
        views.CityCreateView.as_view(),
        name="city_create",
    ),
    path("<int:pk>/", views.CityDetailsView.as_view(), name="city_detail"),
    path(
        "<int:pk>/edit/",
        views.CityEditView.as_view(),
        name="city_update",
    ),
    path(
        "<int:pk>/delete/",
        views.CityDeleteView.as_view(),
        name="city_delete",
    ),
]
