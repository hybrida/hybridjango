from django.views import generic

from .models import Event


class EventList(generic.ListView):
    model = Event
    template_name = 'events/events.html'
    ordering = ['-timestamp']


class EventView(generic.DetailView):
    model = Event
    template_name = 'events/event.html'
