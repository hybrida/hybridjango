from django.db import models
from django.utils import timezone

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