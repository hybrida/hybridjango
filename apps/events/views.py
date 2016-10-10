from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic

from .models import Event


class EventList(generic.ListView):
    model = Event
    template_name = 'events/event_list.html'
    ordering = ['-timestamp']


class EventView(generic.DetailView):
    model = Event
    template_name = 'events/event.html'


class EventCreate(LoginRequiredMixin, generic.CreateView):
    model = Event
    fields = [
        'title',
        'ingress',
        'text',
        'image',
        'max_participants',
        'signup_start',
        'signup_end',
        'event_start',
        'event_end',
    ]
    success_url = ''

    def get_success_url(self):
        return reverse('event', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        event = form.save(commit=False)
        event.author = self.request.user
        return super(EventCreate, self).form_valid(form)


class EventEdit(LoginRequiredMixin, generic.UpdateView):
    model = Event
    fields = [
        'title',
        'ingress',
        'text',
        'image',
        'max_participants',
        'signup_start',
        'signup_end',
        'event_start',
        'event_end',
    ]

    def get_success_url(self):
        return reverse('event', kwargs={'pk': self.object.pk})


class EventDelete(LoginRequiredMixin, generic.DeleteView):
    model = Event
    success_url = reverse_lazy('event_list')


def join_event(request, pk):
    user = request.user
    if user.is_authenticated:
        event = Event.objects.get(pk=pk)
        if event.participants.count() < event.max_participants and event.signup_open():
            event.participants.add(user)
    return redirect('event', pk)


def leave_event(request, pk):
    user = request.user
    if user.is_authenticated and Event.objects.get(pk=pk).signup_open():
        Event.objects.get(pk=pk).participants.remove(user)
    return redirect('event', pk)
