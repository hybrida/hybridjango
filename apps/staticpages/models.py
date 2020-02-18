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
        return "Referat: " + str(self.date)


class BoardReportSemester(models.Model):
    year = models.IntegerField(default=0)
    semester = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.semester + " " + str(self.year)


class Statute(models.Model):
    statute = models.FileField(verbose_name="Statutter", upload_to='pdf/statutter')
    date = models.DateField(verbose_name="Dato (Format: ÅÅÅÅ-MM-DD)", default=timezone.now)

    def __str__(self):
        return "Statutter sist oppdatert: " + str(self.date)


class Protocol(models.Model):
    protocol = models.FileField(upload_to='pdf/protokoll')
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "Protokoll Genfors: " + str(self.date)


class Application(models.Model):
    name = models.CharField(max_length=500, verbose_name="navn")
    sent_by = models.ForeignKey(Hybrid, null=True, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, null=True)
    description = models.TextField(max_length=5000, verbose_name="beskrivelse")

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
        return "Referat: " + str(self.date)


class Updatek(models.Model):
    frontpage = models.FileField(verbose_name="Forsidebilde", upload_to='pdf/updatek')
    pdf = models.FileField(upload_to='pdf/updatek')
    school_year = models.CharField(verbose_name="Skoleår (Eks: 2018-2019 eller 2019-2020)", max_length=50, blank=True)
    edition = models.IntegerField(verbose_name="Utgave nummer")

    def __str__(self):
        return str(self.school_year) + " Utgave: " + str(self.edition)
