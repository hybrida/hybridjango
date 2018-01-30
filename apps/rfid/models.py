from django.db import models

from apps.events.models import Event
from apps.registration.models import Hybrid


class Appearances(models.Model):
    users = models.ManyToManyField(Hybrid, blank=True)
    event = models.OneToOneField(Event, blank=True, on_delete=models.DO_NOTHING, primary_key=True)

    def add_appearance(self, user):
        self.users.add(user)

    def __str__(self):
        return "RFID for event #"+str(self.event.pk)+": "+self.event.title


class GeneralAssembly(models.Model):
    users = models.ManyToManyField(Hybrid, blank=True)
    event = models.OneToOneField(Event, blank=True, on_delete=models.DO_NOTHING, primary_key=True)

    def add_genfors_appearance(self, user):
        self.users.add(user)

    def remove_genfors_appearance(self, user):
        self.users.remove(user)

    def __str__(self):
        return "RFID for generalforsamling: " + str(self.event.pk) + ": " + self.event.title