from django.contrib import admin

from core.models import Theme


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    ...
