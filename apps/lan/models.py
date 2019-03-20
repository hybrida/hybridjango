from django.db import models
from apps.registration.models import Hybrid

class Result(models.Model):
    user = models.name = models.ForeignKey(Hybrid, on_delete=models.CASCADE, null=False, blank=False)
    time = models.DurationField(blank=False, null=False)