from django.db import models
from apps.registration.models import Hybrid
from apps.griffensorden.models import Ridder
from django.urls import reverse

import os

# Create your models here.

# model that contains the basic view functionality for the badges, will have 1to1 link to a certain set of requirements for that badge
class Badge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    badge_image = models.ImageField(upload_to='badges')
    scorepoints = models.PositiveIntegerField()
    user = models.ManyToManyField(Hybrid, blank=True, related_name='hybridbadges')

    def __str__(self):
        return self.name


class BadgeForslag(models.Model):
    navn = models.CharField(max_length=200)
    beskrivelse = models.TextField()
    tildeles = models.CharField(max_length=1000)
    badge_bilde = models.ImageField(upload_to='badges')
    scorepoints = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('scoreboard')


class BadgeRequest(models.Model):
    user = models.ForeignKey(Hybrid, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    reason = models.TextField()

