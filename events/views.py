from django.views.generic import ListView

from events.models import Events


class EventsListView(ListView):
    model = Events
    ordering = "-event_date"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if search := self.request.GET.get("search"):
            queryset = self.model.objects.filter(description__icontains=search)
        return queryset

    def get_template_names(self):
        templates = super().get_template_names()
        if self.request.headers.get("Hx-Request"):
            templates.insert(0, "events/events_table.html")
        return templates
