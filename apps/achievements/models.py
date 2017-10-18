from django.db import models
from apps.registration.models import Hybrid
from apps.griffensorden.models import Ridder
import os

# Create your models here.
# model that enables the creation fo multiple different requirements for the badges
class Prerequisites(models.Model):
    years = models.IntegerField(default=False)
    commite_member = models.BooleanField(default=False)
    hyb_member = models.BooleanField(default=False)
    jub_medal = models.BooleanField(default=False)
    ridder = models.BooleanField(default=False)
    vago = models.BooleanField(default=False)
    simsim = models.BooleanField(default=False)
    participation_badge = models.BooleanField(default=False)
    quiz_winner = models.BooleanField(default=False)
    council_medal = models.BooleanField(default=False)

    def __str__(self):
        return self.pk

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
