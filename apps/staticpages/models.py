from django.db import models
from django.utils import timezone
from django.urls import reverse


class BoardReport(models.Model):
    report = models.FileField(upload_to='pdf/referat')
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "Referat: "+str(self.date)


class Protocol(models.Model):
    protocol = models.FileField(upload_to='pdf/protokoll')
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "Protokoll Genfors: "+str(self.date)


class Application(models.Model):
    navn = models.CharField(max_length=500)
    beskrivelse = models.TextField(max_length=5000)


    def get_absolute_url(self):
        return reverse('about')


class ComApplication(models.Model):
    navn = models.CharField(max_length=500)

    Choices = (
        ('Vevkom', 'Vevkom'),
        ('Bedkom', 'Bedkom'),
        ('Arrkom', 'Arrkom'),
        ('Jentekom', 'Jentekom'),
        ('Kjellerkom', 'Kjellerkom'),
        ('Redaksjonen', 'Redaksjonen')
    )

    komite = models.CharField(choices=Choices, max_length=500)

    def get_absolute_url(self):
        return reverse('about')
