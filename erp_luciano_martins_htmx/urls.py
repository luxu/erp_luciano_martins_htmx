from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("accounts.urls")),
    path('core/', include("core.urls")),
    path('city/', include("city.urls")),
    path('gasto/', include("gasto.urls")),
    path('admin/', admin.site.urls),
]
