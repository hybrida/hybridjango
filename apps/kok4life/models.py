from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=50)


class File(models.Model):
    name = models.CharField(max_length=500)
    file = models.FileField(upload_to='kok')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)