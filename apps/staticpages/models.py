from django.db import models
from django.utils import timezone

class BoardReport(models.Model):
    report = models.FileField(upload_to='pdf/møtereferat')
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return "Referat: "+str(self.date)