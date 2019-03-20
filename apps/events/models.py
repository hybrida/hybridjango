import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from tinymce import HTMLField

from apps.registration.models import Hybrid, Specialization

'''The main event class'''


class Event(models.Model):
    title = models.CharField(max_length=150)
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

    def invited_specialization(self, specialization):
        return not self.specializations.count() or specialization in self.specializations.all()

    def signup_open(self):
        return self.signup_start and self.signup_end and self.signup_start < timezone.now() < self.signup_end

    def signup_has_opened(self):
        return self.signup_start < timezone.now()

    def signup_closed(self):
        return self.signup_start and self.signup_end and timezone.now() > self.signup_end

    def invited(self, user):
        return user.gender in self.genders and str(user.get_grade()) in self.grades and self.invited_specialization(
            user.specialization)

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

    def get_number_of_marks(self, hybrid):  # Finds the number of marks a user has
        marks = Mark.objects.all().filter(recipient=hybrid)
        totalMarks = 0
        for mark in marks:
            totalMarks += mark.value
        return totalMarks

    def too_many_marks(self, hybrid, maxmarks):  # Checks if a user has too many marks to sign up to an event
        if maxmarks != 0 and maxmarks <= self.get_number_of_marks(hybrid):
            return True
        return False

    def goes_on_secondary(self, hybrid, maxmarks,
                          too_many):  # Checks whether a user goes on the secondary waitinglist or not
        if maxmarks != 0 and maxmarks <= self.get_number_of_marks(hybrid) and not self.too_many_marks(hybrid, too_many):
            return True
        return False

    def signup_delay(self, hybrid, delays):  # Finds how many minutes a users signup time is delayed
        for delay in delays:
            if delay.marks <= self.get_number_of_marks(hybrid):
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


'''A model that will contain any feedback or comment that may be instered into the event'''


class EventComment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    author = models.ForeignKey(Hybrid, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    text = models.TextField()

    def __str__(self):
        return '{} - {} - {}'.format(self.event, self.author, self.timestamp)


'''Checks which semester we're in and returns the amount of days to the end of that semester'''


def closest_end_of_semester():
    now = datetime.date.today()
    end_sem1 = datetime.date(now.year, 7, 1)
    end_sem2 = datetime.date(now.year + 1, 1, 1)
    delta = end_sem1 - now
    if delta.days <= 0:
        return (end_sem2 - now).days
    else:
        return delta.days


'''Returns the date of the end of the semester we're in'''


def closest_end_of_semester_date():
    return (datetime.date.today() + datetime.timedelta(days=closest_end_of_semester()))


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
    end = models.DateTimeField(
        default=datetime.datetime.combine(datetime.datetime.now() + datetime.timedelta(days=closest_end_of_semester()),
                                          datetime.datetime.min.time()))
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return '{}, {} - {} dager'.format(self.recipient, self.start, MarkPunishment.objects.all().last().duration)

    # Checks if the mark has passed it's expiredate, if so it deletes it self
    def check_mark(self):
        time = self.end
        if datetime.now >= time:
            self.delete(self)


class Delay(models.Model):
    punishment = models.ForeignKey('MarkPunishment', blank=True, on_delete=models.CASCADE, related_name='+',
                                   default=None)
    marks = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('marks', 'minutes',)
        ordering = ['-marks']


'''A class that contain one or more rule that the markpunishement model uses'''


class Rule(models.Model):
    punishment = models.ForeignKey('MarkPunishment', blank=True, on_delete=models.CASCADE, related_name='+',
                                   default=None)
    rule = models.CharField(max_length=500, blank=True, default='')


'''A model that will contain 1 or more rules that will be implemented on the site'''


class MarkPunishment(models.Model):
    delay = models.ManyToManyField(Delay, blank=True)  # Delays to signup based on the amount of marks a user has
    rules = models.ManyToManyField(Rule, blank=True)  # The rules displayed in the mark.html
    duration = closest_end_of_semester()  # How long a mark lasts
    goes_on_secondary = models.PositiveIntegerField(
        default=0)  # How many marks to put a user on a secondary waitinglist
    too_many_marks = models.PositiveIntegerField(default=0)  # How many marks to block a user from signing up to events
    signoff_close = models.PositiveIntegerField(default=1)  # How many hours before event start does signoff close
