import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views import generic
from django.utils import timezone


from apps.events.forms import EventForm
from apps.rfid.models import Appearances
from .models import Event, EventComment, Attendance, Participation


class EventList(generic.ListView):
    template_name = 'events/events.html'
    paginate_by = 10
    page_kwarg = 'side'

    def get_queryset(self):
        queryset = Event.objects.filter(hidden=False, news=True)
        queryset_not_attendance = queryset.filter(attendance__isnull=True)
        queryset = queryset.filter(attendance__isnull=False)
        queryset_active = queryset.filter(
            attendance__signup_start__lte=timezone.now(),
            attendance__signup_end__gte=timezone.now()
        )
        queryset_not_opened = queryset.filter(
            attendance__signup_start__gt=timezone.now()
        )
        queryset_closed = queryset.filter(
            attendance__signup_end__lt=timezone.now()
        )
        queryset_low_priority = queryset_closed | queryset_not_attendance
        queryset_final = [*queryset_active.order_by("attendance__signup_end"),
                          *queryset_not_opened.order_by("attendance__signup_start"),
                          *queryset_low_priority.order_by("-event_start")
                          ]
        if not self.request.user.is_authenticated:
            # queryset_final = queryset_final.filter(public=True)
            queryset_final = [*filter(lambda e: e.public, queryset_final)]
        return queryset_final


class EventView(generic.DetailView):
    model = Event
    template_name = 'events/event.html'

    def post(self, request, *args, **kwargs):
        attendance = Attendance.objects.get(pk=request.POST['attendance'])
        user = request.user
        if request.POST['action'] == 'leave' and attendance.signup_open:
            #En bruker trykker på "meld av"-knappen, det sjekkes at påmeldingen er åpen og at brukeren faktisk er påmeldt
            if Participation.objects.filter(hybrid=user, attendance=attendance).exists() and attendance.is_signed(user):
                #førstemann på venteliste blir plukket ut og sendt en mail.
                if attendance.get_waiting().exists():
                    first_waiter = attendance.get_waiting()[0]
                    SendAdmittedMail(first_waiter, attendance)
                Participation.objects.filter(hybrid=user, attendance=attendance).delete()
            #Den som meldte seg av blir faktisk avmeldt. Ettersom attendance er en liste som kun skiller venteliste fra påmeldte på antall plasser,
            # vil førstemann på venteliste automatisk bli flyttet til påmeldt.
            elif Participation.objects.filter(hybrid=user, attendance=attendance).exists() and not attendance.is_signed(user):
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
    mail = [hybrid.email if hybrid.email else '{}@stud.ntnu.no'.format(hybrid.username)]
    successful = send_mail(
            'Du har fått plass på {title}'
                .format(title=attendance.event.title),
            'Hei {name},\n\nDet er en glede å meddele at du har fått plass på {title}\n{url}'
                .format(url="https://hybrida.no/hendelser/" + str(attendance.event.pk),
                    title = attendance.event.title,
                    name = hybrid.get_full_name()
                ),
            'robot@hybrida.no',
            mail,
        )

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

