from django.db import models
from apps.registration.models import Hybrid
from django.utils import timezone

from apps.events.models import Event





class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    responsible = models.ForeignKey(Hybrid)
    address = models.CharField(max_length=150, null=True, blank=True)
    info = models.CharField(max_length=300, null=True, blank=True)
    logo = models.ImageField(upload_to='companies', default='placeholder-logo.png')

    CHOICES_STATUS = (
        ('Booket', 'BOOKET'),
        ('Opprettet kontakt', 'KONTAKTET'),
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


class Contact_person(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50, default="99253420")
    job = models.CharField(max_length=100, default="hei")
    company = models.OneToOneField(Company, blank=True, null=True)
    def __str__(self):
        return str(self.name)+" at "+str(self.company)


class Bedpress(models.Model):
    company = models.ForeignKey(Company)
    event = models.OneToOneField(Event)

    def __str__(self):
        return str(self.event)


class CompanyComment(models.Model):
    company = models.ForeignKey(Company)
    author = models.ForeignKey(Hybrid)
    timestamp = models.DateTimeField(default=timezone.now)
    text = models.TextField()

    def __str__(self):
        return str(str(self.author.first_name)+" "+str(self.author.last_name)+" in "+str(self.company)+": "+str(self.text))