from django.shortcuts import render
from city.models import City

def index(request):
    template_name = "index.html"
    cities = City.objects.all()
    context = {
        'cities': [{'id': r.id, 'nome': str(r)} for r in cities[:5]]
    }
    return render(request, template_name, context)
