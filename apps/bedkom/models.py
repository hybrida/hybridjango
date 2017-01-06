from django.db import models
from apps.registration.models import Hybrid
from django.utils import timezone

from apps.events.models import Event


class Contact_person(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    def __str__(self):
        return self.name



class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    contact_person = models.OneToOneField(Contact_person, blank=True, null=True)
    responsible = models.ForeignKey(Hybrid)
    address = models.CharField(max_length=150, null=True, blank=True)
    info = models.CharField(max_length=300, null=True, blank=True)
    description = models.CharField(max_length=400, null=True, blank=True)
    telephone = models.CharField(max_length=30, null=True, blank=True)
    notes = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='companies', default='placeholder-logo.png')

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



class Bedpress(models.Model):
    company = models.ForeignKey(Company)
    event = models.OneToOneField(Event)

class CompanyComment(models.Model):
    company = models.ForeignKey(Company)
    author = models.ForeignKey(Hybrid)
    timestamp = models.DateTimeField(default=timezone.now)
    text = models.TextField()
