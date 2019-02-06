from django.db import models

from apps.registration.models import Hybrid


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=500)
    file = models.FileField(upload_to='kok')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    author = models.ForeignKey(Hybrid, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

