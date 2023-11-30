from django.shortcuts import render

from .models import City
from .forms import CityForm

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView
)

class CityListView(ListView):
    model = City
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()
        return context


def CitySearchView(request):
    template_name = "city/city_table.html"
    query = request.POST.get('q')
    cities = City.objects.filter(description__icontains=query)
    context = {
        'object_list': cities
    }
    return render(request, template_name, context)


class CityCreateView(CreateView):
    model = City
    template_name = "localization/localization_form.html"
    form_class = CityForm
    # success_url = "website/localization/localization_result.html"

def form_valid(self, form):
        context = self.get_context_data()
        # form = context["form"]
        # self.object = form.save()
        # form.instance = self.object
        # form.save()
        return render(self.request, "localization/localization_result.html", context)


class CityDetailsView(DetailView):
    model = City
    # template_name = "localization/city_detail.html"

class CityEditView(UpdateView):
    model = City
    form_class = CityForm

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     forms = context["form"]
    #     self.object = form.save()
    #     forms.instance = self.object
    #     forms.save()
    #     return render(self.request, "localization/localization_result.html", context)


class CityDeleteView(DeleteView):
    model = City
    success_url = "/city"

