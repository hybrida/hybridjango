from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import datetime
from django.forms import forms

from apps.events.models import Event


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    responsible = models.ForeignKey(User)
    contact_person = models.CharField(max_length=150)
    address = models.CharField(max_length=150, null=True, blank=True)
    info = models.CharField(max_length=300, null=True, blank=True)
    description = models.CharField(max_length=400, null=True, blank=True)
    telephone = models.CharField(max_length=30, null=True, blank=True)
    notes = models.CharField(max_length=100, null=True, blank=True)


    CHOICES_STATUS = (
        ('Booket', 'BOOKET'),
        ('Opprettet kontaktet', 'KONTAKTET'),
        ('Takket nei', 'NEI'),
        ('Ikke kontaktet', 'IKKE_KONTAKTET'),
        ('Sendt mail', 'SENDT_MAIL')
    )

    CHOICES_PRIORITY = (
        ('Høy', 'HØY'),
        ('Middels', 'MIDDELS'),
        ('Lav', 'LAV')
    )

    status = models.CharField(choices=CHOICES_STATUS, max_length=20)
    priority = models.CharField(choices=CHOICES_PRIORITY, max_length=20, null=True)

    def __str__(self):
        return self.name


class CompanyComment(models.Model):
    company = models.ForeignKey(Company)
    commenter = models.ForeignKey(User)
    text = models.TextField()
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return "Kommentar " + str(self.pk)

class EarlierBedpresses(models.Model):
    company = models.ForeignKey(Company)
    room = models.CharField(max_length=25, null=True, blank=True)
    date = models.DateField(default=datetime.datetime.now)

class Bedpress(models.Model):
    event = models.OneToOneField(Event)
    company = models.ForeignKey(Company, null=True)


class EarlierBedpresses(models.Model):
    company = models.ForeignKey()
    bedpress = models.ForeignKey(Bedpress, null=True)
