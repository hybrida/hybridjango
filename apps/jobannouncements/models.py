from django.db import models
from apps.registration.models import Hybrid
from django.utils import timezone
from apps.bedkom.models import Company

class Job(models.Model):
    title = models.CharField(max_length=150)
    company = models.ForeignKey(Company)
    deadline = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    priority = models.BooleanField(default=0)
    author = models.ForeignKey(Hybrid)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.title)