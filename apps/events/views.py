import csv

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views import generic
from django.db import transaction
import datetime

from .forms import *
from apps.rfid.models import Appearances
from .models import *
from apps.registration.models import Hybrid


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
            # En bruker trykker på "meld av"-knappen, det sjekkes at påmeldingen er åpen og at brukeren faktisk er påmeldt
            if Participation.objects.filter(hybrid=user, attendance=attendance).exists() and attendance.is_signed(user):
                # førstemann på venteliste blir plukket ut og sendt en mail.
                if attendance.get_waiting().exists():
                    first_waiter = attendance.get_waiting()[0]
                    SendAdmittedMail(first_waiter, attendance)
                Participation.objects.filter(hybrid=user, attendance=attendance).delete()
            # Den som meldte seg av blir faktisk avmeldt. Ettersom attendance er en liste som kun skiller venteliste fra påmeldte på antall plasser,
            # vil førstemann på venteliste automatisk bli flyttet til påmeldt.
            elif Participation.objects.filter(hybrid=user, attendance=attendance).exists() and not attendance.is_signed(
                    user):
                Participation.objects.filter(hybrid=user, attendance=attendance).delete()
        elif request.POST['action'] == 'join' and attendance.can_join(user):
            Participation.objects.get_or_create(hybrid=user, attendance=attendance)

        elif request.POST['action'] == 'leaveSecondary' and attendance.signup_open():
            # En bruker trykker på "meld av"-knappen, det sjekkes at påmeldingen er åpen og at brukeren faktisk er påmeldt
            if ParticipationSecondary.objects.filter(hybrid=user, attendance=attendance).exists():
                ParticipationSecondary.objects.filter(hybrid=user, attendance=attendance).delete()
        elif request.POST['action'] == 'joinSecondary' and attendance.goes_on_secondary(user,
                                                                                        MarkPunishment.objects.all().last().goes_on_secondary,
                                                                                        MarkPunishment.objects.all().last().too_many_marks):
            ParticipationSecondary.objects.get_or_create(hybrid=user, attendance=attendance)

        elif request.POST['action'] == 'leaveLate' and attendance.signoff_open():
            # En bruker trykker på "meld av"-knappen sent, det sjekkes at avmeldingen er åpen og at brukeren faktisk er påmeldt
            if Participation.objects.filter(hybrid=user, attendance=attendance).exists() and attendance.is_signed(user):
                # førstemann på venteliste blir plukket ut og sendt en mail.
                if attendance.get_waiting().exists():
                    first_waiter = attendance.get_waiting()[0]
                    SendAdmittedMail(first_waiter, attendance)
                    Participation.objects.filter(hybrid=user, attendance=attendance).delete()
                elif MarkPunishment.objects.all().last().mark_on_late_signoff:
                    # Gives a mark and sends a mail to the reciever for signing off late when there was no one to take their place
                    SendMarkMail(user, attendance.late_signoff_mark(user))
                    Participation.objects.filter(hybrid=user, attendance=attendance).delete()
                else:
                    Participation.objects.filter(hybrid=user, attendance=attendance).delete()
            # Den som meldte seg av blir faktisk avmeldt. Ettersom attendance er en liste som kun skiller venteliste fra påmeldte på antall plasser,
            # vil førstemann på venteliste automatisk bli flyttet til påmeldt.
            elif Participation.objects.filter(hybrid=user, attendance=attendance).exists() and not attendance.is_signed(
                    user):
                Participation.objects.filter(hybrid=user, attendance=attendance).delete()

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
                'signup_has_opened': attendance.signup_has_opened(),
                'is_participant': attendance.is_participant(user),
                'is_signed': attendance.is_signed(user),
                'is_waiting': attendance.is_waiting(user),
                'waiting_exists': attendance.get_waiting().exists(),
                'placement': attendance.get_placement(user) if attendance.is_participant(user) else None,
                'waiting_placement': attendance.get_placement(
                    user) + 1 - attendance.max_participants if attendance.is_waiting(user) else None,
                'number_of_marks': attendance.get_number_of_marks(user) if user.is_authenticated else 0,
                'too_many_marks': attendance.too_many_marks(user,
                                                            MarkPunishment.objects.all().last().too_many_marks) if user.is_authenticated else False,
                'goes_on_secondary': attendance.goes_on_secondary(user,
                                                                  MarkPunishment.objects.all().last().goes_on_secondary,
                                                                  MarkPunishment.objects.all().last().too_many_marks) if user.is_authenticated else False,
                'signup_delay': attendance.signup_delay(user, Delay.objects.all()) if user.is_authenticated else 0,
                'delay_over': attendance.delay_over(user, Delay.objects.all()) if user.is_authenticated else True,
                'new_signup_time': attendance.new_signup_time(user,
                                                              Delay.objects.all()) if user.is_authenticated else attendance.signup_start,
                'get_sorted_secondary': attendance.get_sorted_secondary() if user.is_authenticated else False,
                'is_participantSecondary': attendance.is_participantSecondary(user) if user.is_authenticated else False,
                'placementSecondary': attendance.get_placementSecondary(user) if attendance.is_participantSecondary(
                    user) else None,
                'waiting_placementSecondary': attendance.get_waiting_placementsSecondary(),
                'get_signoff_close': attendance.get_signoff_close(),
                'signoff_is_open': attendance.signoff_open(),
            } for attendance in list(event.attendance_set.all())]
        return context


def SendAdmittedMail(hybrid, attendance):
    mail = [hybrid.email if hybrid.email else '{}@stud.ntnu.no'.format(hybrid.username)]
    successful = send_mail(
        'Du har fått plass på {title}'
            .format(title=attendance.event.title),
        'Hei {name},\n\nDet er en glede å meddele at du har fått plass på {title}\n{url}'
            .format(url="https://hybrida.no/hendelser/" + str(attendance.event.pk),
                    title=attendance.event.title,
                    name=hybrid.get_full_name()
                    ),
        'robot@hybrida.no',
        mail,
    )


def SendMarkMail(hybrid, mark):
    mail = [hybrid.email if hybrid.email else '{}@stud.ntnu.no'.format(hybrid.username)]
    successful = send_mail(
        'Du er tildelt {value} prikk'
            .format(value=mark.value),
        'Hei {name},\n\nVi vil informere deg om at du er blitt tildelt en prikk pga;\n {reason}\n'
        'Arrangementet det er snakk om er {title}\n'
        'Denne prikken vil du ha til og med {expireDate}\n'
        'Du har totalt {prikker} prikk(er)\n'
        '{urlEvent}\n'
        '{urlPrikker}'.format(urlEvent="https://hybrida.no/hendelser/" + str(mark.event.pk),
                              urlPrikker="https://hybrida.no/hendelser/prikker",
                              name=hybrid.get_full_name(),
                              title=mark.event.title,
                              reason=mark.reason,
                              expireDate=mark.end,
                              prikker=Mark.objects.all().filter(recipient=hybrid)),
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
    marks = Mark.objects.filter(event=event).all()
    users = appearance.users.all()

    if request.method == 'POST':
        if 'givemark' in request.POST:
            print('\n' * 5)
            pk = request.POST.get('givemark')
            participant = Hybrid.objects.get(pk=pk)
            Mark.objects.get_or_create(event=event, recipient=participant, defaults={'value': 1})

        if 'give_mark_all' in request.POST:
            pk = request.POST.get('give_mark_all')
            print(pk)
            participants = Attendance.objects.get(event=event).get_signed()
            for participant in participants:
                if participant not in users:
                    Mark.objects.get_or_create(event=event, recipient=participant, defaults={'value': 1})

    return render(request, "rfid/unattended_list.html",
                  {'event': event, 'attendance': attendance, 'users': users, 'has_rfid': has_rfid, 'marks': marks})


class MarkView(generic.base.TemplateResponseMixin, generic.base.ContextMixin, generic.base.View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = self.request.user

        context.update({
            'End_date': closest_end_of_semester_date(),
            'Goes_on_secondary': MarkPunishment.objects.all().last().goes_on_secondary,
            'Too_many_marks': MarkPunishment.objects.all().last().too_many_marks,
            'Delay': Delay.objects.all().filter(punishment=MarkPunishment.objects.all().last()),
            'Delays': Delay.objects.all().filter(punishment=MarkPunishment.objects.all().last()).order_by('marks'),
            'Duration': MarkPunishment.objects.all().last().duration,
            'Rules': Rule.objects.all().filter(punishment=MarkPunishment.objects.all().last()),
            'Signoff_close': MarkPunishment.objects.all().last().signoff_close,
        })

        return self.render_to_response(context)


class MarkPunishmentEdit(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'events.change_markpunishment'
    model = MarkPunishment
    template_name = 'events/markPunishment_form.html'
    form_class = MarkPunishmentForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(MarkPunishmentEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['rules'] = RuleFormSet(self.request.POST, instance=self.object)
            data['delays'] = DelayFormSet(self.request.POST, instance=self.object)
        else:
            data['rules'] = RuleFormSet(instance=self.object)
            data['delays'] = DelayFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        rules = context['rules']
        delays = context['delays']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if rules.is_valid():
                rules.instance = self.object
                rules.save()
            if delays.is_valid():
                delays.instance = self.object
                delays.save()
        return super(MarkPunishmentEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('edit_mark_punishment', kwargs={'pk': self.object.pk})
