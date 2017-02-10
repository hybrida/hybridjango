from apps.registration.models import Hybrid
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=150)
    ingress = models.CharField(max_length=350, blank=True, default='')
    text = models.TextField(blank=True)
    author = models.ForeignKey(Hybrid, related_name='authored')
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='events', blank=True)
    event_start = models.DateTimeField(null=True, blank=True)
    event_end = models.DateTimeField(null=True, blank=True)
    weight = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)
    news = models.BooleanField(default=True)
    public = models.BooleanField(default=True)

    participants = models.ManyToManyField(Hybrid, related_name='participating', blank=True)
    waiting_list = models.ManyToManyField(Hybrid, related_name='waiting', blank=True, )
    max_participants = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=50, blank=True)
    signup_start = models.DateTimeField(null=True, blank=True)
    signup_end = models.DateTimeField(null=True, blank=True)
    genders = models.CharField(max_length=3, default='MFU')
    grades = models.CharField(max_length=5, default='12345')

    def get_absolute_url(self):
        if(self.pk < 0): # TODO: replace this
            return 'http://teknologiporten.no/nb/arrangement/' + self.text
        return reverse('event', kwargs={'pk': self.pk})

    def signup_open(self):
        return self.signup_start and self.signup_end and self.signup_start < timezone.now() < self.signup_end

    def signup_closed(self):
        return self.signup_start and self.signup_end and timezone.now() > self.signup_end

    def invited(self, user):
        if self.signup_open:
            return user.gender in self.genders and str(user.get_grade()) in self.grades

    def get_first_waiting(self):
        return self.waiting_list.order_by('id').first()

    def can_join(self, user):
        wait = self.waiting_list.count() and not user.username == self.get_first_waiting()
        return self.signup_open() and self.participants.count() < self.max_participants and self.invited(user) and not wait


    def __str__(self):
        return '{}: {}'.format(self.timestamp.date(), self.title)


class EventComment(models.Model):
    event = models.ForeignKey(Event)
    author = models.ForeignKey(Hybrid)
    timestamp = models.DateTimeField(default=timezone.now)
    text = models.TextField()
