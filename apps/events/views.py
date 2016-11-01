import os
from hybridjango.settings import STATIC_FOLDER
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from apps.events.forms import EventForm
from .models import Event, EventComment


class EventList(generic.ListView):
    model = Event
    template_name = 'events/event_list.html'
    ordering = ['-timestamp']


class EventView(generic.DetailView):
    model = Event
    template_name = 'events/event.html'


class EventCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'events.event.can_add_event'
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(EventCreate, self).form_valid(form)


class EventEdit(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'events.event.can_change_event'
    model = Event
    form_class = EventForm


class EventDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'events.event.can_delete_event'
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


UPDATEK = os.path.join(STATIC_FOLDER, 'pdf/updatek')


def updatek(request):
    context = {}
    dirs = os.listdir(UPDATEK)
    context['updatek'] = sorted([(
                              dir,
                              set([os.path.splitext(file)[0] for file in os.listdir(os.path.join(UPDATEK, dir))])
                          ) for dir in dirs], key=lambda dir: dir[0], reverse=True)
    return render(request, 'staticpages/updatek.html', context)
