from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from apps.events.forms import EventForm
from .models import Event, EventComment


class EventList(generic.ListView):
    model = Event
    template_name = 'events/events.html'

    def get_queryset(self):
        queryset = Event.objects.filter(hidden=False, news=True).order_by('-weight', '-timestamp')
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(public=True)
        return queryset


class EventView(generic.DetailView):
    model = Event
    template_name = 'events/event.html'

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        user = self.request.user
        event = context['event']
        if user in event.waiting_list.all():
            waiting_position = event.waiting_list.filter(id__lt=event.waiting_list.get(id=user.pk).pk).count() + 1
        else:
            waiting_position = 0
        if user.is_authenticated:
            context['invited'] = event.invited(self.request.user)
            context['can_join'] = event.can_join(self.request.user)
            context['waiting_position'] = waiting_position
        return context


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
    event = Event.objects.get(pk=pk)
    if user.is_authenticated and user not in event.participants.all():
        if event.can_join(user):
            event.participants.add(user)
            event.waiting_list.remove(user)
        elif event.invited(user):
            event.waiting_list.add(user)
    return redirect('event', pk)


@login_required
def leave_event(request, pk):
    user = request.user
    event = Event.objects.get(pk=pk)
    if user.is_authenticated and event.signup_open():
        event.participants.remove(user)
        event.waiting_list.remove(user)
        if event.waiting_list.count():
            first_waiting = event.get_first_waiting()
            if event.can_join(first_waiting):
                event.participants.add(first_waiting)
                event.waiting_list.remove(first_waiting)
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
