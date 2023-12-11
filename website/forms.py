import os

from django import forms
from django.forms.models import inlineformset_factory

# from django.utils.translation import ugettext_lazy as _

# from crispy_forms.bootstrap import FormActions, InlineField
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import (
#     HTML,
#     Button,
#     Column,
#     Div,
#     Field,
#     Layout,
#     Row,
#     Submit,
# )

from . import models


class MyDateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        super().__init__(format="%Y-%m-%d")


class BaseMeta:
    exclude = ("deleted", "status")


class HoraTrabalhadaForm(forms.ModelForm):
    class Meta:
        model = models.HoraTrabalhada
        exclude = ["status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PecasForm(forms.ModelForm):
    class Meta(BaseMeta):
        model = models.Pecas


# class ImportForm(forms.Form):
#     import_file = forms.FileField(label=_("File to import"))
#     input_format = forms.ChoiceField(
#         label=_("Format"),
#         choices=(),
#     )
#
#     def __init__(self, import_formats, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#         choices = []
#         for i, f in enumerate(import_formats):
#             choices.append(
#                 (
#                     str(i),
#                     f().get_title(),
#                 )
#             )
#         if len(import_formats) > 1:
#             choices.insert(0, ("", "---"))
#
#         self.fields["input_format"].choices = choices
#         self.helper.layout = Layout(
#             Div(
#                 Row(
#                     Column("import_file", wrapper_class="col-md-12"),
#                 ),
#             ),
#             Div(
#                 Row(
#                     Column("input_format", wrapper_class="col-md-12"),
#                 ),
#             ),
#         )
#
#         self.helper.layout.append(
#             Div(
#                 FormActions(
#                     Submit("submit", "Enviar", css_class="btn btn-primary")
#                 )
#             ),
#         )
#
#
# class ConfirmImportForm(forms.Form):
#     import_file_name = forms.CharField(widget=forms.HiddenInput())
#     original_file_name = forms.CharField(widget=forms.HiddenInput())
#     input_format = forms.CharField(widget=forms.HiddenInput())
#
#     def clean_import_file_name(self):
#         data = self.cleaned_data["import_file_name"]
#         data = os.path.basename(data)
#         return data
#
#
# class ItensPecasForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Div(
#                 Field("description", wrapper_class="col-md-3"),
#                 Field("price", wrapper_class="col-md-3"),
#                 Field("quantity", wrapper_class="col-md-3"),
#                 Field("subtotal", wrapper_class="col-md-3"),
#             )
#         )
#
#     class Meta(BaseMeta):
#         model = models.Itenspecas
#
#
# class ComercioForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Div(Field("description"), wrapper_class="col-md-12"),
#             Div(
#                 FormActions(
#                     Submit("submit", _("Submit"), css_class="btn btn-primary"),
#                     css_class="col-sd-12",
#                 )
#             ),
#         )
#
#     class Meta(BaseMeta):
#         model = models.Comercio
#
#
# ItemPecasFormSet = inlineformset_factory(
#     models.Pecas,
#     models.Itenspecas,
#     form=ItensPecasForm,
#     fields=["description", "pecas", "price", "quantity", "subtotal"],
#     extra=1,
#     can_delete=True,
# )
#
#
# class RabbiitForm(forms.ModelForm):
#     class Meta(BaseMeta):
#         model = models.Rabbiit
#         fields = [
#             "description",
#             "rate_hour",
#             "time_end",
#             "time_start",
#             "time_total",
#             "rate_total",
#         ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#         self.fields["time_start"].widget = forms.HiddenInput()
#         self.fields["time_end"].widget = forms.HiddenInput()
#         self.fields["time_total"].widget = forms.HiddenInput()
#
#         self.helper.layout = Layout(
#             "description",
#             "rate_hour",
#             "time_end",
#             "time_start",
#             "time_total",
#             Div(
#                 Button(
#                     "start_timer",
#                     "Start",
#                     css_id="start_timer",
#                     css_class="btn btn-primary",
#                     onclick="",
#                 ),
#                 Button(
#                     "end_timer",
#                     "Stop",
#                     css_id="end_timer",
#                     css_class="btn btn-success",
#                 ),
#             ),
#             InlineField(
#                 Div(
#                     HTML(
#                         "<span class='show-time' id='show_time_initial'></span>"
#                     ),
#                     HTML("<span class='show-time' id='show_time'></span>"),
#                     HTML(
#                         "<span class='show-time' id='show_time_result'></span>"
#                     ),
#                 ),
#             ),
#             Div(
#                 Submit(
#                     "submit",
#                     ("Enviar"),
#                 ),
#             ),
#         )
#
#     def save(self, commit=True):
#         o = super().save(commit=False)
#         t_tempo = self.cleaned_data["time_total"].minute
#         price = float(self.cleaned_data["rate_hour"].price.replace(",", "."))
#         result = t_tempo / 60 * price
#         self.instance.rate_total = result
#         if commit:
#             o.save()
#         return o
#
#
# class EventsForm(forms.ModelForm):
#     class Meta:
#         model = models.Events
#         fields = [
#             "description", "event_date"
#         ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#         self.fields["event_date"].localize = True
#         self.fields["event_date"].widget = MyDateInput()
#
#         self.helper.layout = Layout(
#             Div(
#                 # Field("description", wrapper_class="col-md-12"),
#                 # Field("event_date", wrapper_class="col-md-12"),
#             ),
#             Div(
#                 FormActions(
#                     Submit("submit", _("Submit"), css_class="btn btn-primary"),
#                     css_class="col-md-12",
#                 )
#             ),
#         )
#
#
class CityForm(forms.ModelForm):
    class Meta:
        model = models.City
        fields = ["description"]


#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Div(
#                 Field("description", wrapper_class="col-md-12"),
#             ),
#             Div(
#                 FormActions(
#                     Submit("submit", _("Submit"), css_class="btn btn-primary"),
#                     css_class="col-md-12",
#                 )
#             ),
#         )
#
#
# class VivoForm(forms.Form):
#     file = forms.FileField()
#
#     class Meta:
#         model = models.Vivo
#         fields = [
#             "file",
#             "velocity",
#             "event_date",
#             "internet_used_in_percentagem",
#             "internet_available_in_percentagem",
#             "internet_used_in_number",
#             "internet_available_in_number",
#             "time",
#             "price",
#         ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#         self.helper.layout = Layout(
#             Div(
#                 Field(
#                     "file",
#                     accept=".txt, .tiff|image/*",
#                     wrapper_class="col-md-12",
#                 ),
#             ),
#             Div(
#                 FormActions(
#                     Submit("submit", _("Submit"), css_class="btn btn-primary"),
#                     css_class="col-md-12",
#                 )
#             ),
#         )
#
#
# class VivoForms(forms.Form):
#     class Meta:
#         model = models.Vivo
#         fields = ["file"]
#
#
# class EmpresaForm(forms.ModelForm):
#     class Meta:
#         model = models.Empresa
#         fields = [
#             "name",
#             "site",
#             "amount_applied",
#             "consulting",
#             "company_culture",
#         ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Div(
#                 Field("name", wrapper_class="col-md-12"),
#                 Field("site", wrapper_class="col-md-12"),
#                 Field("consulting", wrapper_class="col-md-6"),
#                 Field("amount_applied", wrapper_class="col-md-6"),
#                 Field("company_culture", wrapper_class="col-md-12"),
#             ),
#             Div(
#                 FormActions(
#                     Submit("submit", _("Submit"), css_class="btn btn-primary"),
#                     css_class="col-md-12",
#                 )
#             ),
#         )
#
#
# class CustomMMCF(forms.ModelMultipleChoiceField):
#     def label_from_instance(self, skill):
#         return f"{skill.description}"
#
#
# class EmpregoForm(forms.ModelForm):
#
#     skills = CustomMMCF(
#         queryset=models.Skill.objects.all(), widget=forms.CheckboxSelectMultiple
#     )
#
#     class Meta:
#         model = models.Emprego
#         fields = [
#             "company",
#             "entrade_date",
#             "job",
#             "requisite",
#             "skills",
#             "feedback",
#             "feedback_date",
#             "process_fase",
#             "vacancy_found",
#             "count_day_contact",
#         ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#         self.fields["entrade_date"].localize = True
#         self.fields["entrade_date"].widget = MyDateInput()
#         self.fields["feedback_date"].localize = True
#         self.fields["feedback_date"].widget = MyDateInput()
#         self.fields["requisite"].widget.attrs["rows"] = 4
#         self.fields["requisite"].widget.attrs["columns"] = 15
#         # self.fields['skills'].queryset = models.Skill.objects.all()
#
#         self.helper.layout = Layout(
#             Div(
#                 Field("company", wrapper_class="col-md-6"),
#                 Field("entrade_date", wrapper_class="col-md-6"),
#                 Field("job", wrapper_class="col-md-12"),
#                 Field("requisite", wrapper_class="col-md-12"),
#                 Field("skills", wrapper_class="col-md-12"),
#                 Field("feedback", wrapper_class="col-md-4"),
#                 Field("feedback_date", wrapper_class="col-md-3"),
#                 Field("process_fase", wrapper_class="col-md-3"),
#                 Field("vacancy_found", wrapper_class="col-md-3"),
#                 Field("count_day_contact", wrapper_class="col-md-3"),
#             ),
#             Div(
#                 FormActions(
#                     Submit("submit", _("Submit"), css_class="btn btn-primary"),
#                     css_class="col-md-12",
#                 )
#             ),
#         )
#
#
# class SkillsForm(forms.ModelForm):
#     class Meta:
#         model = models.Skill
#         exclude = ["status"]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Div(
#                 Field("description", wrapper_class="col-md-12"),
#             ),
#             Div(
#                 FormActions(
#                     Submit("submit", _("Submit"), css_class="btn btn-primary"),
#                     css_class="col-md-12",
#                 )
#             ),
#         )
#
#
# class ConsultancyForm(forms.ModelForm):
#     class Meta:
#         model = models.Consultancy
#         exclude = ["status"]
#
#     def clean_name(self):
#         name = self.cleaned_data["name"]
#         if [
#             r["name"]
#             for r in models.Consultancy.objects.all().values("name")
#             if r["name"] in name.capitalize()
#         ]:
#             msg = f"Consultoria..:{name} já existe na base!"
#             self.add_error("name", msg)
#         return name
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Div(
#                 Field("name", wrapper_class="col-md-12"),
#                 Field("quantity_of_company", wrapper_class="col-md-12"),
#             ),
#             Div(
#                 FormActions(
#                     Submit("submit", _("Submit"), css_class="btn btn-primary"),
#                     css_class="col-md-12",
#                 )
#             ),
#         )
