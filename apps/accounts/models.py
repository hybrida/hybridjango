import os

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def five_years():
    return timezone.now().year + 5


class Hybrid(models.Model):
    def user_folder(instance, filename):
        return os.path.join('users', instance.user.username, filename)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50, blank=True)
    graduation_year = models.IntegerField(default=five_years)
    image = models.ImageField(upload_to=user_folder, default='placeholder-profile.jpg')
    gender = models.CharField(max_length=20, blank=True)

    def get_full_name(self):
        if self.middle_name:
            first_name = self.user.first_name + ' ' + self.middle_name
        else:
            first_name = self.user.first_name
        return first_name + ' ' + self.user.last_name

    def __str__(self):
        return self.user.username
