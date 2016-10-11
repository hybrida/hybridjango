from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import datetime
from django.forms import forms


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    responsible = models.ForeignKey(User)
    contact_person = models.CharField(max_length=150)

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

    status = models.CharField(choices=CHOICES_STATUS, max_length=15)
    priority = models.CharField(choices=CHOICES_PRIORITY, max_length=10, null=True)

    def __str__(self):
        return self.name


class CompanyComment(models.Model):
    company = models.ForeignKey(Company)
    commenter = models.ForeignKey(User)
    text = models.TextField()
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return "Kommentar " + str(self.pk)