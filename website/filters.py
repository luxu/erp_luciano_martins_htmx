from django import forms

import django_filters

from accounts import constants
from website.models import City, Comercio


class CityField(django_filters.ModelChoiceFilter):
    def get_queryset(self, request):
        """
        Limit results to City's owned by the current user.
        If the current user is not authenticated, return empty queryset.
        """
        if request.user.is_authenticated:
            return City.objects.all()
        return City.objects.none()


class PecasFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name="data",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        lookup_expr="lt",
        label="Start Date",
    )
    end_date = django_filters.DateFilter(
        field_name="data",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        lookup_expr="gt",
        label="End Date",
    )
    # veiculo = django_filters.ChoiceFilter(
    #     choices=constants.TYPE_VEHICLE,
    #     field_name="veiculo",
    #     lookup_expr="exact",
    #     label="Veículo",
    # )
    # proxtroca = django_filters.NumberFilter()
    # troca = django_filters.NumberFilter()
    comercio = django_filters.ChoiceFilter(
        choices=[], field_name="comercio", lookup_expr="exact", label="Comércio"
    )
    # city = django_filters.ChoiceFilter(
    #     choices=[], field_name="city", lookup_expr="exact", label="Cidade"
    # )
    # city = django_filters.ModelChoiceFilter(
    #     # queryset=City.objects.all(),
    #     widget=CityWidget,
    # )

    # total = django_filters.CharFilter(lookup_expr="icontains", label="Total")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.filters["data"].extra["widget"] = forms.DateTimeField()
        # self.filters["veiculo"].extra["widget"] = forms.Select(
        #     attrs={"class": "select form-control form-control-sm"}
        # )
        # self.filters["proxtroca"].extra["widget"] = forms.TextInput(
        #     attrs={"class": "form-control  col-md-6 mb-0"}
        # )
        # self.filters["troca"].extra["widget"] = forms.TextInput(
        #     attrs={"class": "form-control text-center", "max-length": "100"}
        # )
        self.filters["comercio"].extra["choices"] = [
            (obj_comercio.id, obj_comercio.description)
            for obj_comercio in Comercio.objects.all()
        ]
        self.filters["comercio"].extra["widget"] = forms.Select(
            attrs={"class": "select form-control form-control-sm"}
        )
        # self.filters["city"].extra["choices"] = [
        #     (obj_city.id, obj_city.description) for obj_city in City.objects.all()
        # ]
        # self.filters["city"].extra["widget"] = forms.Select(
        #     attrs={"class": "select form-control form-control-sm"}
        # )
        # self.filters["total"].extra["widget"] = forms.TextInput(
        #     attrs={"class": "form-control text-center", "max-length": "100"}
        # )
