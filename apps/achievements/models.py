from django.db import models
from apps.registration.models import Hybrid
from apps.griffensorden.models import Ridder
import os

# Create your models here.
# model that enables the creation fo multiple different requirements for the badges
class Prerequisites(models.Model):
    years = models.IntegerField(default=0)
    commite_member = models.BooleanField(default=0)
    hyb_member = models.BooleanField(default=0)
    jub_medal = models.BooleanField(default=0)
    ridder = models.BooleanField(default=0)
    vago = models.BooleanField(default=0)
    simsim = models.BooleanField(default=0)
    participation_badge = models.BooleanField(default=0)
    quiz_winner = models.BooleanField(default=0)

    def __str__(self):
        return self.name

# model that contains the basic view functionality for the badges, will have 1to1 link to a certain set of requirements for that badge
class Badge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    badge_image = models.FileField(upload_to='badges/')
    badge_placeholder = models.FileField(upload_to='badges/')
    scorepoints = models.IntegerField()
    user = models.ManyToManyField(Hybrid, default=None)
    prereq = models.OneToOneField(Prerequisites, default=None)

    def __str__(self):
        return self.name
