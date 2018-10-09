from django.db import models

class Subjects(models.Model):
    name = models.CharField(max_length=50)
    subject = models.ForeignKey('Files', on_delete=models.CASCADE)


class Files(models.Model):
    name = models.CharField(max_length=500)
    file = models.FileField(upload_to='kok')