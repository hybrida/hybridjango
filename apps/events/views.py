import csv

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views import generic
from django.db import transaction
from datetime import datetime, timedelta

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
        mark_punishment = MarkPunishment.objects.last()

        if request.POST['action'] == 'leave' and attendance.signup_open():
            # The "sign off"-button was pushed, checks if the user is signed up and if the signup is still open
            if Participation.objects.filter(hybrid=user, attendance=attendance).exists() and attendance.is_signed(user):
                # The first waiter is picked out and gets sent a mail telling them they got a spot in the event
                if attendance.get_waiting().exists():
                    first_waiter = attendance.get_waiting()[0]
                    SendAdmittedMail(first_waiter, attendance)
                Participation.objects.filter(hybrid=user, attendance=attendance).delete()
            # The user that signed off is actually removed. As attendance is just a single list dividing the waiting
            # list from the participants by the index, the first person in line automatically becomes a participant.
            elif Participation.objects.filter(hybrid=user, attendance=attendance).exists() and not attendance.is_signed(
                    user):
                Participation.objects.filter(hybrid=user, attendance=attendance).delete()
        elif request.POST['action'] == 'join' and attendance.can_join(user):
            Participation.objects.get_or_create(hybrid=user, attendance=attendance)

        elif request.POST['action'] == 'leaveSecondary' and attendance.signup_open():
            # The "secondary sign off"button was pushed, checks if the user is signed up and if the signup is still open
            if ParticipationSecondary.objects.filter(hybrid=user, attendance=attendance).exists():
                ParticipationSecondary.objects.filter(hybrid=user, attendance=attendance).delete()
        elif request.POST['action'] == 'joinSecondary' and attendance.goes_on_secondary(
                user, mark_punishment.goes_on_secondary, mark_punishment.too_many_marks):
            ParticipationSecondary.objects.get_or_create(hybrid=user, attendance=attendance)

        elif request.POST['action'] == 'leaveLate' and attendance.signoff_open():
            # The "late sign off"-button was pushed, checks if the user is signed up and if the sign off is still open
            if Participation.objects.filter(hybrid=user, attendance=attendance).exists() and attendance.is_signed(user):
                # The first waiter is picked out and gets sent a mail telling them they got a spot in the event
                if attendance.get_waiting().exists():
                    first_waiter = attendance.get_waiting()[0]
                    SendAdmittedMail(first_waiter, attendance)
                elif mark_punishment.mark_on_late_signoff and attendance.event.type.use_mark_on_late_signoff:
                    # Gives a mark and sends a mail to the user for signing off late when no one could take their place
                    SendMarkMail(user, late_signoff_mark(hybrid=user, event=attendance.event))
                Participation.objects.filter(hybrid=user, attendance=attendance).delete()

            elif Participation.objects.filter(hybrid=user, attendance=attendance).exists() \
                    and not attendance.is_signed(user):
                # Checks if the user is on he waiting list
                Participation.objects.filter(hybrid=user, attendance=attendance).delete()

        self.object = self.get_object()
        return self.render_to_response(context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        user = self.request.user
        mark_p = MarkPunishment.objects.last()
        delays = Delay.objects.filter(punishment=mark_p)
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
                'number_of_marks': get_number_of_marks(user) if user.is_authenticated else 0,
                'too_many_marks': attendance.too_many_marks(user, mark_p.too_many_marks)
                if user.is_authenticated else False,
                'goes_on_secondary': attendance.goes_on_secondary(user, mark_p.goes_on_secondary, mark_p.too_many_marks)
                if user.is_authenticated else False,
                'signup_delay': attendance.signup_delay(user, delays) if user.is_authenticated else 0,
                'delay_over': attendance.delay_over(user, delays) if user.is_authenticated else True,
                'new_signup_time': attendance.new_signup_time(
                    user, delays) if user.is_authenticated else attendance.signup_start,
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


def SendRemovedMail(hybrid, attendance, reason):
    mail = [hybrid.email if hybrid.email else '{}@stud.ntnu.no'.format(hybrid.username)]
    successful = send_mail(
        'Du har mistet plassen din på {title}'
            .format(title=attendance.event.title),
        'Hei {name},\n\nDu har mistet plassen din på {title}\n{url}\nFordi {reason}'
            .format(url="https://hybrida.no/hendelser/" + str(attendance.event.pk),
                    title=attendance.event.title,
                    name=hybrid.get_full_name(),
                    reason=reason,
                    ),
        'robot@hybrida.no',
        mail,
    )


def SendMarkMail(hybrid, mark):
    mail = [hybrid.email if hybrid.email else '{}@stud.ntnu.no'.format(hybrid.username)]
    successful = send_mail(
        'Du er tildelt {value} prikk'
            .format(value=mark.value),
        'Hei {name},\n\nVi vil informere deg om at du er blitt tildelt en prikk pga.;\n'
        '   {reason}\n'
        'Arrangementet det er snakk om er {title}, {urlEvent}.\n'
        'Denne prikken vil du ha til og med {expireDate}.\n'
        'Du har totalt {prikker} prikk(er).\n'
        'For mer informasjon angående regler og konsekvenser for prikksystenet gå til {urlPrikker}'
            .format(urlEvent="https://hybrida.no/hendelser/" + str(mark.event.pk),
                    urlPrikker="https://hybrida.no/hendelser/prikker",
                    name=hybrid.get_full_name(),
                    title=mark.event.title,
                    reason=mark.reason,
                    expireDate=mark.end,
                    prikker=get_number_of_marks(hybrid)),
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
            mark, created = Mark.objects.get_or_create(event=event, recipient=participant, defaults={'value': 1},
                                                       reason="Du møtte ikke opp på arrangementet")
            SendMarkMail(participant, mark)
            remove_user_from_events(participant)

        if 'give_mark_all' in request.POST:
            pk = request.POST.get('give_mark_all')
            print(pk)
            participants = Attendance.objects.get(event=event).get_signed()
            for participant in participants:
                if participant not in users:
                    mark, created = Mark.objects.get_or_create(event=event, recipient=participant,
                                                               defaults={'value': 1},
                                                               reason="Du møtte ikke opp på arrangementet")
                    SendMarkMail(participant, mark)
                    remove_user_from_events(participant)

    return render(request, "rfid/unattended_list.html",
                  {'event': event, 'attendance': attendance, 'users': users, 'has_rfid': has_rfid, 'marks': marks})


def late_signoff_mark(event, hybrid):
    mark, created = Mark.objects.get_or_create(
        recipient=hybrid, value=1, event=event,
        reason="Du meldte deg sent av et arrangement hvor det ikke var noen på venteliste.")
    remove_user_from_events(hybrid)
    return mark


def remove_user_from_events(hybrid):
    num_marks = get_number_of_marks(hybrid)
    mark_punishment = MarkPunishment.objects.last()
    too_many_marks = mark_punishment.too_many_marks
    if num_marks >= too_many_marks != 0 and mark_punishment.remove_on_too_many_marks:
        # Gets all attendance objects from today to one year from now and
        # where the user is either a participant or on the secondary waitinglist.
        attendances = hybrid.hybridattendances.filter(
            event__event_start__range=[datetime.now(), datetime.now() + timedelta(days=365)])
        attendances_secondary = hybrid.hybridattendances_secondary.filter(
            event__event_start__range=[datetime.now(), datetime.now() + timedelta(days=365)])

        for attendance in attendances:
            if attendance.event.type.use_remove_on_too_many_marks:
                # Checks if the person that is being removed is on the waitinglist,
                # if not it sends mail to the first person on the waiting list
                if attendance.get_waiting().exists() and not attendance.is_waiting(hybrid):
                    first_waiter = attendance.get_waiting()[0]
                    SendAdmittedMail(first_waiter, attendance)
                Participation.objects.filter(hybrid=hybrid, attendance=attendance).delete()
                SendRemovedMail(hybrid, attendance, 'du har for mange prikker.')

        for attendance in attendances_secondary:
            if attendance.event.type.use_remove_on_too_many_marks:
                ParticipationSecondary.objects.filter(hybrid=hybrid, attendance=attendance).delete()
                SendRemovedMail(hybrid, attendance, 'du har for mange prikker.')

    return


class MarkView(generic.base.TemplateResponseMixin, generic.base.ContextMixin, generic.base.View):
    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        mark_punishment = MarkPunishment.objects.last()
        delays = Delay.objects.filter(punishment=mark_punishment)
        rules = Rule.objects.filter(punishment=mark_punishment)

        context.update({
            'End_date': end_of_semester(),
            'Goes_on_secondary': mark_punishment.goes_on_secondary,
            'Too_many_marks': mark_punishment.too_many_marks,
            'Delay': delays.first(),
            'Delays': delays.order_by('marks'),
            'Duration': mark_punishment.duration,
            'Rules': rules,
            'Signoff_close': mark_punishment.signoff_close,
            'Mark_on_late_signoff': mark_punishment.mark_on_late_signoff,
            'Remove_on_too_many_marks': mark_punishment.remove_on_too_many_marks,
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
