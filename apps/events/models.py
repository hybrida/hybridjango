import datetime

from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils import timezone
from tinymce import HTMLField

from apps.registration.models import Hybrid, Specialization

'''Defines rules for different type of events'''


class EventType(models.Model):
    name = models.CharField(max_length=150)

    # Can choose which parts of the Mark Systems are active for a specific type of event
    use_delay = models.BooleanField(default=False)
    use_goes_on_secondary = models.BooleanField(default=False)
    use_too_many_marks = models.BooleanField(default=False)
    use_mark_on_late_signoff = models.BooleanField(default=False)
    use_remove_on_too_many_marks = models.BooleanField(default=False)

    def __str__(self):
        return self.name


'''The main event class'''


class Event(models.Model):
    title = models.CharField(max_length=150)
    type = models.ForeignKey(EventType, default=1, null=False, on_delete=models.CASCADE)
    ingress = models.CharField(max_length=350, blank=True, default='')
    text = HTMLField(blank=True)
    author = models.ForeignKey(Hybrid, related_name='authored', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='events', blank=True)
    event_start = models.DateTimeField(null=True, blank=True)
    event_end = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=50, blank=True)
    weight = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)
    news = models.BooleanField(default=True)
    public = models.BooleanField(default=True)
    signoff_close = models.PositiveIntegerField(default=None, null=True, blank=True)
    signoff_close_on_signup_close = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('event', kwargs={'pk': self.pk})

    def is_bedpress(self):
        from apps.bedkom.models import Bedpress
        return Bedpress.objects.filter(event=self).exists()

    def __str__(self):
        return '{}: {}'.format(self.timestamp.date(), self.title)


'''A special kind of event, pulled from Teknologiportens site'''


class TPEvent(models.Model):
    tp_id = models.IntegerField(default=0, unique=True)
    title = models.CharField(max_length=150)
    event_start = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return 'http://teknologiporten.no/nb/arrangement/{}'.format(self.tp_id)


'''the sign up class, adds a Hybrid to the signed up list'''


class Participation(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    hybrid = models.ForeignKey(Hybrid, on_delete=models.CASCADE)
    attendance = models.ForeignKey('Attendance', on_delete=models.CASCADE)
    excursion = models.BooleanField(default=False)

    class Meta:
        unique_together = ('hybrid', 'attendance')
        ordering = ['timestamp']

    def __str__(self):
        return '{timestamp}-{hybrid}-{attendance}'.format(hybrid=self.hybrid, attendance=self.attendance,
                                                          timestamp=self.timestamp)


'''A secondary wait list for those users that already have a mark, functions the same as participation'''


class ParticipationSecondary(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    hybrid = models.ForeignKey(Hybrid, on_delete=models.CASCADE)
    attendance = models.ForeignKey('Attendance', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('hybrid', 'attendance')
        ordering = ['timestamp']

    def __str__(self):
        return '{timestamp}-{hybrid}-{attendance}'.format(hybrid=self.hybrid, attendance=self.attendance,
                                                          timestamp=self.timestamp)


'''the main participation model, links the primary and secondary waiting list. It also defines who will be able to 
attend the event, price and so forth'''


class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='Påmelding')
    participants = models.ManyToManyField(Hybrid, blank=True, through=Participation, related_name='+')
    participantsSecondary = models.ManyToManyField(Hybrid, blank=True, through=ParticipationSecondary, related_name='+')
    max_participants = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    signup_start = models.DateTimeField()
    signup_end = models.DateTimeField()
    genders = models.CharField(max_length=3, default='MFU')
    grades = models.CharField(max_length=50, default='12345')
    specializations = models.ManyToManyField(Specialization, blank=True, limit_choices_to={'active': True})
    groups = models.ManyToManyField(Group, blank=True)

    def invited_specialization(self, specialization):
        return not self.specializations.count() or specialization in self.specializations.all()

    def invited_groups(self, groups):
        if not self.groups.count():
            return True
        for group in groups:
            if group in self.groups.all():
                return True
        return False

    def signup_open(self):
        return self.signup_start and self.signup_end and self.signup_start < timezone.now() < self.signup_end

    def signup_has_opened(self):
        return self.signup_start < timezone.now()

    def get_event_name(self):
        return self.event.title

    def get_event_start(self):
        return self.event.event_start

    def get_event_pk(self):
        return self.event.pk

    def signup_closed(self):
        return self.signup_start and self.signup_end and timezone.now() > self.signup_end

    def invited(self, user):
        return user.gender in self.genders and str(user.get_grade()) in self.grades and self.invited_specialization(
            user.specialization) and self.invited_groups(user.groups.all())

    def get_sorted_hybrids(self):
        return self.participants.order_by('participation__timestamp')

    def get_signed(self):
        return self.get_sorted_hybrids()[:self.max_participants]

    def get_waiting(self):
        return self.get_sorted_hybrids()[self.max_participants:]

    def full(self):
        return self.participants.count() >= self.max_participants

    def can_join(self, user):
        return self.signup_open() and self.invited(user)

    def get_placements(self):
        return enumerate(self.get_sorted_hybrids())

    def get_waiting_placements(self):
        return [(index + 1 - self.max_participants, participant)
                for (index, participant)
                in self.get_placements()
                if index >= self.max_participants]

    def get_placement(self, hybrid):
        for index, participant in self.get_placements():
            if participant == hybrid:
                return index
        raise ValueError('Hybrid is not a participant')

    def is_participant(self, hybrid):
        return self.participants.filter(pk=hybrid.pk).exists()

    def is_signed(self, hybrid):
        if self.is_participant(hybrid):
            return self.get_placement(hybrid) < self.max_participants
        return False

    def is_waiting(self, hybrid):
        if self.is_participant(hybrid):
            return self.get_placement(hybrid) >= self.max_participants
        return False

    def clean(self):
        if self.signup_end and self.signup_start and self.signup_end < self.signup_start:
            raise ValidationError('Påmeldingen kan ikke slutte før den har begynt.')

    def __str__(self):
        return '{}, {}'.format(self.name, self.event)

    def too_many_marks(self, hybrid, maxmarks):  # Checks if a user has too many marks to sign up to an event
        if self.event.type.use_too_many_marks:
            if maxmarks != 0 and maxmarks <= get_number_of_marks(hybrid):
                return True
        return False

    def goes_on_secondary(self, hybrid, maxmarks, too_many):  # Checks whether a user goes on the secondary
        if self.event.type.use_goes_on_secondary:  # waitinglist or not
            if maxmarks != 0 and maxmarks <= get_number_of_marks(hybrid) and not self.too_many_marks(hybrid, too_many):
                return True
        return False

    def signup_delay(self, hybrid, delays):  # Finds how many minutes a users signup time is delayed
        if self.event.type.use_delay:
            for delay in delays:
                if delay.marks <= get_number_of_marks(hybrid):
                    return delay.minutes
        return 0

    def delay_over(self, hybrid, delays):  # Checks if signup delay is over
        if self.new_signup_time(hybrid, delays) < timezone.now():
            return True
        return False

    def new_signup_time(self, hybrid, delays):  # Checks at what time a user can signup to an event
        return self.signup_start + datetime.timedelta(minutes=self.signup_delay(hybrid, delays))

    def get_sorted_secondary(self):  # Returns a sorted secondary waitinglist
        return self.participantsSecondary.order_by('participationsecondary__timestamp')

    def is_participantSecondary(self, hybrid):  # Checks if a user is on the secondary waitinglist
        return self.participantsSecondary.filter(pk=hybrid.pk).exists()

    def get_placementsSecondary(self):
        return enumerate(self.get_sorted_secondary())

    def get_placementSecondary(self, hybrid):
        for index, participantsSecondary in self.get_placementsSecondary():
            if participantsSecondary == hybrid:
                return index + 1
        raise ValueError('Hybrid is not a participant')

    def get_waiting_placementsSecondary(self):
        return [(index + 1, participant)
                for (index, participant)
                in self.get_placementsSecondary()]

    def get_signoff_close(self):
        if MarkPunishment.objects.all().last().signoff_close is None and self.event.signoff_close is None:
            return self.signup_end
        elif self.event.signoff_close_on_signup_close is True:
            return self.signup_end
        elif self.event.signoff_close is not None:
            return self.event.event_start - datetime.timedelta(hours=self.event.signoff_close)
        return self.event.event_start - datetime.timedelta(hours=MarkPunishment.objects.all().last().signoff_close)

    def signoff_open(self):
        return self.get_signoff_close() > timezone.now()


'''A model that will contain any feedback or comment that may be instered into the event'''


class EventComment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    author = models.ForeignKey(Hybrid, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    text = models.TextField()

    def __str__(self):
        return '{} - {} - {}'.format(self.event, self.author, self.timestamp)


'''Checks which semester we're in and returns the date of the end of that semester'''


def end_of_semester():
    today = datetime.date.today()
    end_autumn = datetime.date(today.year + 1, 1, 1)
    end_spring = datetime.date(today.year, 7, 1)
    if end_spring > today:
        return end_spring
    else:
        return end_autumn


'''Returns the amount of days untill the end of the semester'''


def end_of_semester_days():
    return (end_of_semester() - datetime.date.today()).days


'''Returns the total amount of marks a user has'''


def get_number_of_marks(hybrid):  # Finds the number of marks a user has
    marks = Mark.objects.all().filter(recipient=hybrid)
    totalMarks = 0
    for mark in marks:
        totalMarks += mark.value
    return totalMarks


'''A model that contains a mark given to users for transgressions in accordance with the rules regarding events'''


class Mark(models.Model):
    @staticmethod
    def num_marks(user):
        num = 0
        for mark in Mark.objects.all().filter(recipient=user):
            num += mark.value
        return num

    recipient = models.ForeignKey(Hybrid, on_delete=models.CASCADE)
    value = models.IntegerField()
    start = models.DateTimeField(default=timezone.now)
    end = models.DateField(default=end_of_semester)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return '{}, {} - {} dager'.format(self.recipient, self.start, MarkPunishment.objects.all().last().duration)

    # Checks if the mark is at or passed it's expiredate, if so it deletes itself
    def check_mark(self):
        if datetime.date.today() >= self.end:
            self.delete()


class Delay(models.Model):
    punishment = models.ForeignKey('MarkPunishment', blank=True, on_delete=models.CASCADE, related_name="has_delays",
                                   default=None)
    marks = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('marks', 'minutes',)
        ordering = ['-marks']


'''A class that contain one or more rule that the markpunishement model uses'''


class Rule(models.Model):
    punishment = models.ForeignKey('MarkPunishment', blank=True, on_delete=models.CASCADE, related_name="has_rules",
                                   default=None)
    rule = models.CharField(max_length=500, blank=True, default='')


'''A model that will contain 1 or more rules that will be implemented on the site'''


class MarkPunishment(models.Model):
    delay = models.ManyToManyField(Delay, blank=True)  # Delays to signup based on the amount of marks a user has
    rules = models.ManyToManyField(Rule, blank=True)  # The rules displayed in the mark.html
    duration = end_of_semester_days()  # How long a mark lasts
    goes_on_secondary = models.PositiveIntegerField(
        default=0)  # How many marks to put a user on a secondary waitinglist
    too_many_marks = models.PositiveIntegerField(default=0)  # How many marks to block a user from signing up to events
    signoff_close = models.PositiveIntegerField(default=None, null=True,
                                                blank=True)  # How many hours before event start does signoff close
    mark_on_late_signoff = models.BooleanField(default=True)  # If a mark is given or not for signing off late
    remove_on_too_many_marks = models.BooleanField(
        default=True)  # If a user has too many marks, they will be removed from future events
