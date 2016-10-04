from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    responsible = models.ForeignKey(User)
    contact_person = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class CompanyComment(models.Model):
    company = models.ForeignKey(Company)
    commenter = models.ForeignKey(User)
    text = models.TextField()
    timestamp = models.DateTimeField()
