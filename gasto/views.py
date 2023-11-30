from django.shortcuts import render

from django.shortcuts import render

from .models import Gasto
from .forms import GastoForm

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView
)

class GastoListView(ListView):
    model = Gasto
    # template_name = "localization/localization_list.html"
    # template_name_suffix = '_list'
    # context_object_name = "localidades"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()
        return context


def GastoSearchView(request):
    template_name = "gasto/gasto_table.html"
    query = request.POST.get('q')
    cities = Gasto.objects.filter(description__icontains=query)
    context = {
        'object_list': cities
    }
    return render(request, template_name, context)


class GastoCreateView(CreateView):
    model = Gasto
    template_name = "localization/localization_form.html"
    form_class = GastoForm
    # success_url = "website/localization/localization_result.html"

def form_valid(self, form):
        context = self.get_context_data()
        # form = context["form"]
        # self.object = form.save()
        # form.instance = self.object
        # form.save()
        return render(self.request, "localization/localization_result.html", context)


class GastoDetailsView(DetailView):
    model = Gasto
    # template_name = "localization/gasto_detail.html"

class GastoEditView(UpdateView):
    model = Gasto
    form_class = GastoForm

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     forms = context["form"]
    #     self.object = form.save()
    #     forms.instance = self.object
    #     forms.save()
    #     return render(self.request, "localization/localization_result.html", context)


class GastoDeleteView(DeleteView):
    model = Gasto
    success_url = "/gasto"
