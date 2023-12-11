from django import forms
from django.forms.models import inlineformset_factory

# from django.utils.translation import ugettext_lazy as _
#
from .models_gasto_segmento import Cardbank, Gasto, Parcelas, Segmento


#
#
# class MyDateInput(forms.DateInput):
#     input_type = "date"
#
#     def __init__(self, **kwargs):
#         super().__init__(format="%Y-%m-%d")
#
#
# class BaseMeta:
#     exclude = ("deleted", "status")
#
#
class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = "__all__"


#         widgets = {
#             "datagasto": DatePickerWidget(
#                 attrs={"format": "dd/mm/yyyy", "icon": "fa-calendar"}
#             ),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#         self.helper.layout = Layout(
#             Row(
#                 Column("name", css_class="form-group col-md-12 mb-0"),
#                 Column("more_infos", css_class="form-group col-md-12 mb-0"),
#                 Column(
#                     "description_on_invoice",
#                     css_class="form-group col-md-12 mb-0",
#                 ),
#                 Column("datagasto", css_class="form-group col-md-4 mb-0"),
#                 Column("segmento", css_class="form-group col-md-4 mb-0"),
#                 Column("opcoes_cartao", css_class="form-group col-md-4 mb-0"),
#                 Column("card_bank", css_class="form-group col-md-4 mb-0"),
#                 css_class="form-row",
#             )
#         )
#
#
# class ParcelasForm(forms.ModelForm):
#
#     data_parcela = forms.DateField(localize=True, widget=MyDateInput())
#
#     class Meta(BaseMeta):
#         model = Parcelas
#         widgets = {
#             "data_parcela": DatePickerWidget(
#                 attrs={"format": "dd/mm/yyyy", "icon": "fa-calendar"}
#             ),
#         }
#         exclude = ()
#
#
# ParcelasFormSet = inlineformset_factory(
#     Gasto,
#     Parcelas,
#     form=ParcelasForm,
#     extra=0,
#     can_delete=True,
#     fields=["parcelas", "numero_parcela", "valor_parcela", "data_parcela"],
# )
#
#
# class SegmentoForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#         self.helper.attrs = {"novalidate": ""}
#
#         self.helper.layout = Layout(
#             Div(
#                 Row(Column("name", css_class="form-group col-md-12 mb-0")),
#                 FormActions(
#                     Submit(
#                         "submit",
#                         _("Submit"),
#                     ),
#                     css_class="form-group col-md-12 mb-0",
#                 ),
#             )
#         )
#
#     class Meta(BaseMeta):
#         model = Segmento
#
#
# class CardbankForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#         self.helper.attrs = {"novalidate": ""}
#
#         self.helper.layout = Layout(
#             Div(
#                 Row(Column("name", css_class="form-group col-md-12 mb-0")),
#                 FormActions(
#                     Submit(
#                         "submit",
#                         _("Submit"),
#                     ),
#                     css_class="form-group col-md-12 mb-0",
#                 ),
#             )
#         )
#
#     class Meta(BaseMeta):
#         model = Cardbank
