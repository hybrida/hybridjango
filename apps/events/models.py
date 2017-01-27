from apps.registration.models import Hybrid
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=150)
    ingress = models.CharField(max_length=350, blank=True, default='')
    text = models.TextField()
    author = models.ForeignKey(Hybrid, related_name='authored')
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='events', default='placeholder-event.png')
    participants = models.ManyToManyField(Hybrid, related_name='participating', blank=True)
    max_participants = models.IntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=50, blank=True)
    signup_start = models.DateTimeField(null=True, blank=True)
    signup_end = models.DateTimeField(null=True, blank=True)
    event_start = models.DateTimeField(null=True, blank=True)
    event_end = models.DateTimeField(null=True, blank=True)
    weight = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)
    news = models.BooleanField(default=True)

    def get_absolute_url(self):
        if(self.pk < 0): # TODO: replace this
            return 'http://teknologiporten.no/nb/arrangement/' + self.text
        return reverse('event', kwargs={'pk': self.pk})

    def signup_open(self):
        return self.signup_start and self.signup_end and self.signup_start < timezone.now() < self.signup_end

    def signup_closed(self):
        return self.signup_start and self.signup_end and timezone.now() > self.signup_end

    def __str__(self):
        return '{}: {}'.format(self.timestamp.date(), self.title)


class EventComment(models.Model):
    event = models.ForeignKey(Event)
    author = models.ForeignKey(Hybrid)
    timestamp = models.DateTimeField(default=timezone.now)
    text = models.TextField()
