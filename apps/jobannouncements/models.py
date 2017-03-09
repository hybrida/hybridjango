from django.db import models
from apps.registration.models import Hybrid
from django.utils import timezone
from apps.bedkom.models import Company

class Job(models.Model):
    title = models.CharField(max_length=150)
    company = models.ForeignKey(Company)
    deadline = models.DateTimeField(null=True)
    description = models.TextField(blank=True, null=True, default="")
    ingress = models.CharField(max_length=250, default="", blank=True)
    link = models.CharField(max_length=150, blank=True, default="")
    weight = models.IntegerField(default=0)
    priority = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)