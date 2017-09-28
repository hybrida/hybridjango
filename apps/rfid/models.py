from django.db import models

from apps.events.models import Event
from apps.registration.models import Hybrid


class Appearances(models.Model):
    users = models.ManyToManyField(Hybrid, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.DO_NOTHING, unique=True)

    def add_appearance(self, user):
        self.users.add(user)
