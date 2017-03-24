from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.registration.models import Hybrid, Specialization


class Event(models.Model):
    title = models.CharField(max_length=150)
    ingress = models.CharField(max_length=350, blank=True, default='')
    text = models.TextField(blank=True)
    author = models.ForeignKey(Hybrid, related_name='authored')
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
        if (self.pk < 0):  # TODO: replace this
            return 'http://teknologiporten.no/nb/arrangement/' + self.text
        return reverse('event', kwargs={'pk': self.pk})

    def __str__(self):
        return '{}: {}'.format(self.timestamp.date(), self.title)


class Participation(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    hybrid = models.ForeignKey(Hybrid)
    attendance = models.ForeignKey('Attendance')
    excursion = models.BooleanField(default=False)

    class Meta:
        unique_together = ('hybrid', 'attendance')

    def __str__(self):
        return '{timestamp}-{hybrid}-{attendance}'.format(hybrid=self.hybrid, attendance=self.attendance,
                                                          timestamp=self.timestamp)


class Attendance(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=50, default='Påmelding')
    participants = models.ManyToManyField(Hybrid, blank=True, through=Participation)
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

    def signup_closed(self):
        return self.signup_start and self.signup_end and timezone.now() > self.signup_end

    def invited(self, user):
        return user.gender in self.genders and str(user.get_grade()) in self.grades and self.invited_specialization(
            user.specialization)

    def get_signed(self):
        return Participation.objects.filter(attendance_id=self).order_by('-timestamp')[:self.max_participants]

    def get_waiting(self):
        return Participation.objects.filter(attendance_id=self).order_by('-timestamp')[self.max_participants:]

    def full(self):
        return self.participants.count() >= self.max_participants

    def can_join(self, user):
        return self.signup_open() and self.invited(user)

    def get_placements(self):
        return enumerate(self.participants.order_by('participation__timestamp'))

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

    def __str__(self):
        return '{}, {}'.format(self.name, self.event)


class EventComment(models.Model):
    event = models.ForeignKey(Event)
    author = models.ForeignKey(Hybrid)
    timestamp = models.DateTimeField(default=timezone.now)
    text = models.TextField()
