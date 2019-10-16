from django.db import models

from apps.registration.models import Hybrid


# TODO: Split name into course_id and name, schema migration, data migration
class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)
    author = models.ForeignKey(Hybrid, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=500)
    file = models.FileField(upload_to='hybridopedia')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    author = models.ForeignKey(Hybrid, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
