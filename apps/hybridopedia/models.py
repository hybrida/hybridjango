from django.core.validators import RegexValidator
from django.db import models
import os

from apps.registration.models import Hybrid, Subject


class File(models.Model):
    def get_path(self, file_name):
        new_file_name = file_name.replace('æ', 'ae')
        new_file_name = new_file_name.replace('ø', 'oe')
        new_file_name = new_file_name.replace('å', 'aa')
        return os.path.join("hybridopedia", self.subject.name, new_file_name)

    name = models.CharField(max_length=500)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    author = models.ForeignKey(Hybrid, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to=get_path)

    def __str__(self):
        return self.name
