import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views import generic

from apps.events.forms import EventForm
from apps.rfid.models import Appearances
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
            if Participation.objects.filter(hybrid=user, attendance=attendance).exists() and attendance.is_signed(user):
                first_waiter = attendance.get_waiting()[0]
                SendAdmittedMail(first_waiter, attendance)
                print("\n\n\n " + first_waiter.first_name +" \n\n\n ")
            Participation.objects.filter(hybrid=user, attendance=attendance).delete()
        elif request.POST['action'] == 'join' and attendance.can_join(user):
            Participation.objects.get_or_create(hybrid=user, attendance=attendance)

        self.object = self.get_object()
        return self.render_to_response(context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        user = self.request.user
        event = context['event']
        has_rfid = Appearances.objects.filter(event=event).exists()
        context['has_rfid'] = has_rfid
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

def SendAdmittedMail(hybrid, attendance):
    print("\n\n HEI HEI \n\n")
    mail = ['{}@stud.ntnu.no'.format(hybrid.username)]
    if hybrid.email: mail = hybrid.email
    print("\n\n Klarte dette også gitt \n\n")
    mail = hybrid.email
    print("\n\n")
    print(mail)
    print("\n\n")
    successful = send_mail(
            'Du har fått plass på {title}',
            'Hei {name},\n\nDet er en glede å meddele at du har fått plass på {title}\n'
            '{url}'.format(            url="https://hybrida.no/hendelser/" + str(attendance.event.pk),
            title = attendance.event.title,
            name = hybrid.get_full_name()),
            'robot@hybrida.no',
            mail,
        )
    print("\n\n")
    print(successful)
    print("\n\n")

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
    events = Event.objects.filter(hidden=False)
    if not request.user.is_authenticated:
        events = events.filter(public=True)
    events.filter()
    return JsonResponse([{
        'title': event.title,
        'start': event.event_start,
        'end': event.event_end,
        'url': "../hendelser/" + str(event.pk),
        'allDay': False
    } for event in events if event.event_start is not None], safe=False)

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


def signed(request, pk):
    event = Event.objects.filter(pk=pk).first()
    has_rfid = Appearances.objects.filter(event=event).exists()
    attendance = Attendance.objects.filter(event=event)
    return render(request, "rfid/signed_list.html", {'event': event, 'attendance': attendance, 'has_rfid': has_rfid})


def attended(request, pk):
    event = Event.objects.filter(pk=pk).first()
    has_rfid = Appearances.objects.filter(event=event).exists()
    appearance = Appearances.objects.filter(event=event).first()
    users = appearance.users.all()
    return render(request, "rfid/attended_list.html", {'event': event, 'users': users, 'has_rfid': has_rfid})


def unattended(request, pk):
    event = Event.objects.filter(pk=pk).first()
    attendance = Attendance.objects.filter(event=event)
    appearance = Appearances.objects.filter(event=event).first()
    has_rfid = Appearances.objects.filter(event=event).exists()
    users = appearance.users.all()
    return render(request, "rfid/unattended_list.html", {'event': event, 'attendance': attendance, 'users': users, 'has_rfid': has_rfid})

