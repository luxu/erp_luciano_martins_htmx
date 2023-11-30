from django import forms
from core.models import City

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = "__all__"
