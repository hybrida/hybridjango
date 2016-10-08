import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import datetime


class Event(models.Model):
    @staticmethod
    def path_and_name(self, instance, filename):
        return os.path.join('users', '{}{}'.format(instance.pk, filename.split('.')[-1]))

    title = models.CharField(max_length=150)
    ingress = models.CharField(max_length=500)
    text = models.TextField()
    author = models.ForeignKey(User)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    image = models.ImageField(upload_to=path_and_name, default='placeholder-event.png')
    participants = models.ManyToManyField(User)

    signup_start = models.DateTimeField()
    signup_end = models.DateTimeField()
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
