import os
from django.db import models
from django.contrib.auth.models import User


class Hybrid(models.Model):
    def user_folder(instance, filename):
        return os.path.join('users', instance.user.username, filename)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50)
    graduation_year = models.IntegerField()
    image = models.ImageField(upload_to=user_folder, default='placeholder-profile.jpg')
    gender = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username