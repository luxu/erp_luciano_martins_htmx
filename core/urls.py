from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # path('user_settings/', views.userSettings, name="user_settings"),
    path('', views.update_theme, name="update_theme")
]
