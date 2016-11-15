from django.db import models
from apps.registration.models import Hybrid

class Team(models.Model):
    name = models.CharField(max_length=100)
    points = models.FloatField()
    image = models.ImageField(upload_to='quiz', default='placeholder-event.png')

    def __str__(self):
        return self.name