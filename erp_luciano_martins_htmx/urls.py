from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("core/", include("core.urls")),
    path("city/", include("city.urls")),
    path("gasto/", include("gasto.urls")),
    path("events/", include("events.urls")),
]
