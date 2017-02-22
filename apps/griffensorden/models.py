from django.db import models
from apps.registration.models import Hybrid
from django.utils import timezone
import datetime

class Ridder(models.Model):
    name = models.CharField(max_length=200)
    finished = models.CharField(max_length=4)
    awarded = models.CharField(max_length=4)
    description = models.TextField()

    def __str__(self):
        return self.name

class Honary_member(models.Model):
    name = models.CharField(max_length=200)
    awarded = models.CharField(max_length=4)
    description = models.TextField()

    def __str__(self):
        return self.name