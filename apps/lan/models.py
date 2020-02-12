from django.db import models

# Create your models here.
from apps.registration.models import Hybrid


class Scoreboard(models.Model):
    pass


class Entry(models.Model):
    user = models.ForeignKey(Hybrid, null=False, blank=False)
    value = models.DoubleField(null=False, blank=False)
    scoreboard = models.ForeignKey(Scoreboard, related_name='entries', blank=False)


