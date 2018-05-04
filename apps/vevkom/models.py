from django.db import models
from django.utils import timezone
from django.urls import reverse
from tinymce import HTMLField


# Create your models here.

class CakeMaker(models.Model):
    name = models.CharField(max_length=100)
    number_on_list = models.IntegerField(unique=True)

    def __str__self(self):
        return "Commite_member"+str(self.name)

    class Meta:
        ordering = ['-number_on_list']


class MeetingReport(models.Model):
    date = models.DateField(default=timezone.now)
    tilstede = models.CharField(max_length=200)
    text = models.TextField(max_length=3000)

    def __str__self(self):
        return "Referat: " + str(self.date)

class Project(models.Model):
    name = models.CharField(max_length=50)
    responsible = models.CharField(max_length=500)
    description = models.CharField(max_length=3000)

    Choices_Status = (
        ('Påbegynt','Påbegynt'),
        ('Ikke Påbegynt','Ikke Påbegynt'),
        ('Ferdig','Ferdig')
    )

    Choices_Priority = (
        ('Høy', 'Høy'),
        ('Middels', 'Middels'),
        ('Lav', 'Lav')
    )

    status = models.CharField(choices=Choices_Status, max_length=100)
    priority = models.CharField(choices=Choices_Priority, max_length= 100)

    def __str__self(self):
        return str(self.name)



class Guide(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=50000)

    def __str__(self):
        return str(self.name)


