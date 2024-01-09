from django.shortcuts import redirect
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="home"),
    path("logout/", lambda request: redirect("/admin/logout", permanent=False)),
]
