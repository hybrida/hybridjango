from django.db import models
from apps.registration.models import Hybrid
from apps.griffensorden.models import Ridder
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
