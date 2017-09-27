import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from apps.events.forms import EventForm
from .models import Event, EventComment, Attendance, Participation


class EventList(generic.ListView):
    model = Event
    template_name = 'events/events.html'
    ordering = ('-weight', '-event_start')
    paginate_by = 10
    page_kwarg = 'side'

    def get_queryset(self):
        queryset = super(EventList, self).get_queryset().filter(hidden=False, news=True)
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(public=True)
        return queryset


class EventView(generic.DetailView):
    model = Event
    template_name = 'events/event.html'

    def post(self, request, *args, **kwargs):
        attendance = Attendance.objects.get(pk=request.POST['attendance'])
        user = request.user
        if request.POST['action'] == 'leave' and attendance.signup_open():
            Participation.objects.filter(hybrid=user, attendance=attendance).delete()
        elif request.POST['action'] == 'join' and attendance.can_join(user):
            Participation.objects.get_or_create(hybrid=user, attendance=attendance)

        self.object = self.get_object()
        return self.render_to_response(context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        user = self.request.user
        event = context['event']
        context['attendances'] = [
            {
                'o': attendance,
                'is_invited': attendance.invited(user) if user.is_authenticated else False,
                'can_join': attendance.can_join(user) if user.is_authenticated else False,
                'is_participant': attendance.is_participant(user),
                'is_signed': attendance.is_signed(user),
                'is_waiting': attendance.is_waiting(user),
                'placement': attendance.get_placement(user) if attendance.is_participant(user) else None,
                'waiting_placement': attendance.get_placement(
                    user) + 1 - attendance.max_participants if attendance.is_waiting(user) else None,
            } for attendance in list(event.attendance_set.all())]
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


def calendar_api(request):
    return JsonResponse([{
        'title': event.title,
        'start': event.event_start,
        'end': event.event_end,
        'allDay': False
    } for event in Event.objects.all()], safe=False)

@login_required
def participants_csv(request, pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(pk)
    writer = csv.writer(response)
    for attendance in Event.objects.get(pk=pk).attendance_set.all():
        writer.writerow((attendance.name,))
        writer.writerow([
            'Navn',
            'Trinn',
            'Spesialisering',
            'Kjønn',
            'Matpreferanser',
            'Epost',
        ])
        for participant in attendance.get_signed():
            writer.writerow([
                participant.get_full_name(),
                participant.get_grade(),
                participant.specialization,
                participant.gender,
                participant.food_preferences,
                participant.username + "@stud.ntnu.no",
            ])
    return response


@login_required
def comment_event(request, pk):
    user = request.user
    if request.POST:
        event_id = request.POST['event_id']
        text = request.POST['text']
        if user.is_authenticated:
            comment = EventComment(author=user, event_id=event_id, text=text)
            comment.save()
    return redirect('event', pk)


@login_required
def delete_comment_event(request, pk):
    user = request.user
    if request.POST and 'delete' in request.POST:
        comment = EventComment.objects.get(pk=request.POST['delete'])
        if user.is_authenticated and comment.author == user:
            comment.delete()
    return redirect('event', pk)
