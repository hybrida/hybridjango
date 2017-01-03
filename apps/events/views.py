import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from apps.events.forms import EventForm
from .models import Event, EventComment


class EventList(generic.ListView):
    model = Event
    template_name = 'events/events.html'
    queryset = Event.objects.filter(hidden=False).order_by('-weight', '-timestamp')

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context['event_list_chronological'] = Event.objects.filter(
            event_start__gte=timezone.now()
        ).order_by('event_start')[:5]
        return context


class EventView(generic.DetailView):
    model = Event
    template_name = 'events/event.html'


class EventCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'events.add_event'
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(EventCreate, self).form_valid(form)


class EventEdit(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'events.change_event'
    model = Event
    form_class = EventForm


class EventDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'events.delete_event'
    model = Event
    success_url = reverse_lazy('event_list')


@login_required
def join_event(request, pk):
    user = request.user
    if user.is_authenticated:
        event = Event.objects.get(pk=pk)
        if event.participants.count() < event.max_participants and event.signup_open():
            event.participants.add(user)
    return redirect('event', pk)


@login_required
def leave_event(request, pk):
    user = request.user
    if user.is_authenticated and Event.objects.get(pk=pk).signup_open():
        Event.objects.get(pk=pk).participants.remove(user)
    return redirect('event', pk)


@login_required
def comment_event(request, pk):
    user = request.user
    if request.POST:
        event_id = request.POST['event_id']
        text = request.POST['text']
        if user.is_authenticated:
            comment = EventComment(author=user, event_id=event_id, text=text)
            print(comment.full_clean())
            comment.save()
    return redirect('event', pk)

