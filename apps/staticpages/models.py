from django.db import models
from django.utils import timezone
from django.urls import reverse
from apps.registration.models import Hybrid


class BoardReport(models.Model):
    report = models.FileField(upload_to='pdf/referat')
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=50, blank=True)
    semester = models.ForeignKey('BoardReportSemester', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Referat: "+str(self.date)

class BoardReportSemester(models.Model):
    year = models.IntegerField(default=0)
    semester = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.semester + " " + str(self.year)

class Protocol(models.Model):
    protocol = models.FileField(upload_to='pdf/protokoll')
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "Protokoll Genfors: "+str(self.date)


class Application(models.Model):
    navn = models.CharField(max_length=500)
    beskrivelse = models.TextField(max_length=5000)


    Grants = (
        ('Støttet', 'Støttet'),
        ('Delvis støttet', 'Delvis støttet'),
        ('Ikke støttet', 'Ikke støttet')
    )
    granted = models.CharField(choices=Grants, blank=True, max_length=500)
    comment = models.TextField(max_length=5000, blank=True)

    def get_absolute_url(self):
        return reverse('about')


class CommiteApplication(models.Model):
    navn = models.ForeignKey(Hybrid, on_delete=models.CASCADE)

    Choices = (
        ('Vevkom', 'Vevkom'),
        ('Bedkom', 'Bedkom'),
        ('Arrkom', 'Arrkom'),
        ('Jentekom', 'Jentekom'),
        ('Kjellerkom', 'Kjellerkom'),
        ('Redaksjonen', 'Redaksjonen'),
        ('Prokom', 'Prokom')
    )

    prioritet_1 = models.CharField(choices=Choices, max_length=500)
    prioritet_2 = models.CharField(choices=Choices, blank=True, max_length=500)
    prioritet_3 = models.CharField(choices=Choices, blank=True, max_length=500)
    prioritet_4 = models.CharField(choices=Choices, blank=True, max_length=500)
    kommentar = models.TextField(blank=True, max_length=1000)

    def get_absolute_url(self):
        return reverse('about')


class Ktv_report(models.Model):
    report = models.FileField(upload_to='pdf/ITVreferat')
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "Referat: "+str(self.date)