from django.db import models
from apps.registration.models import Hybrid
from apps.registration.models import Specialization
import datetime


class Course(models.Model):
    temp_field = models.CharField(max_length=10, null=True)


class Evaluation(models.Model):
    temp_field = models.CharField(max_length=10, null=True)
