from django.db import models
from apps.registration.models import Hybrid
from django.utils import timezone

from apps.events.models import Event





class Company(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Navn')
    responsible = models.ForeignKey(Hybrid, verbose_name='Bedriftskontakt')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Adresse')
    info = models.CharField(max_length=300, null=True, blank=True, verbose_name='Ingress')
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

    status = models.CharField(choices=CHOICES_STATUS, max_length=20, verbose_name='Status')
    priority = models.CharField(choices=CHOICES_PRIORITY, max_length=20, null=True, verbose_name='Prioritet')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Bedrift'
        verbose_name_plural  = 'Bedrifter'



class Contact_person(models.Model):
    name = models.CharField(max_length=50, verbose_name='Navn')
    email = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50, default="99253420", verbose_name='Telefon')
    job = models.CharField(max_length=100, default="hei", verbose_name='Stilling')
    company = models.OneToOneField(Company, blank=True, null=True, verbose_name='Bedrift')
    def __str__(self):
        return str(self.name)+" at "+str(self.company)


    class Meta:
        verbose_name = 'Kontaktperson'
        verbose_name_plural  = 'Kontaktpersoner'



class Bedpress(models.Model):
    company = models.ForeignKey(Company)
    event = models.OneToOneField(Event)
    verbose_name = "Bedriftspresentasjoner"

    def __str__(self):
        return str(self.company.name) + " den " + str(self.event)



    class Meta:
        verbose_name = 'Bedriftspresentasjon'
        verbose_name_plural  = 'Bedriftspresentasjoner'


class CompanyComment(models.Model):
    company = models.ForeignKey(Company)
    author = models.ForeignKey(Hybrid)
    timestamp = models.DateTimeField(default=timezone.now)
    text = models.TextField()

    def __str__(self):
        return str(str(self.author.first_name)+" "+str(self.author.last_name)+" in "+str(self.company)+": "+str(self.text))