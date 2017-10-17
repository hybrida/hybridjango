from django.db import models
from apps.registration.models import Hybrid
import os

# Create your models here.
class Badge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    badge_image = models.FileField(upload_to='badges/')
    badge_placeholder = models.FileField(upload_to='badges/')
    scorepoints = models.IntegerField()
    user = models.ManyToManyField(Hybrid, default=None)

    def __str__(self):
        return self.name
