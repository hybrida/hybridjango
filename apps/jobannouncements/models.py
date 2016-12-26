from django.db import models
from apps.bedkom.models import Company

class Job(models.Model):
    title = models.CharField(max_length=150)
    Company = models.ForeignKey(Company)
    deadline = models.DateTimeField(null=True, blank=True)
    descripion = models.TextField()
    priority = models.IntegerField(default=0)
    logo = models.ImageField(upload_to='companies', default='placeholder-event.png')

    def __str__(self):
        return str(self.title)