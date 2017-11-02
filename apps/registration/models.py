from datetime import timedelta

import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import RegexValidator



def get_graduation_year(grade):
    return five_years() - int(grade)


def five_years():
    return (timezone.now() + timedelta(weeks=26)).year + 5


def user_folder(instance, filename):
    return os.path.join('users', instance.username, filename)


class Specialization(models.Model):
    name = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True, blank=False, null=False)

    def __str__(self):
        return self.name


class Hybrid(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Mellomnavn')
    member = models.BooleanField(default=False, verbose_name='Medlem')
    graduation_year = models.IntegerField(default=five_years, verbose_name='Avgangsår')
    image = models.ImageField(upload_to=user_folder, default='placeholder-profile.jpg', verbose_name='Bilde')
    gender = models.CharField(max_length=1, blank=False, choices=(('M', 'Mann'), ('F', 'Dame'), ('U', 'Ukjent')),
                              verbose_name='Kjønn', default='U')
    specialization = models.ForeignKey(Specialization, null=False, default=1, on_delete=models.SET_DEFAULT,
                                       verbose_name='Spesialisering')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Fødselsår')
    title = models.CharField(max_length=150, blank=True, default='Hybrid', verbose_name='Tittel')
    food_preferences = models.CharField(max_length=150, blank=True, verbose_name='Allergier og matpreferanser')
    card_key = models.CharField(max_length=10, null=True, blank=True, unique=True, verbose_name='NTNU-kortkode')

    def get_full_name(self):
        if self.middle_name:
            first_name = self.first_name + ' ' + self.middle_name
        else:
            first_name = self.first_name
        if first_name == "" and self.last_name == "":
            return self.username
        return first_name + ' ' + self.last_name
    full_name = property(get_full_name)

    def get_grade(self):
        return five_years() - self.graduation_year

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.username})


class RecoveryMail(models.Model):
    hybrid = models.ForeignKey(Hybrid)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return "{}_{}".format(self.hybrid, self.timestamp)
