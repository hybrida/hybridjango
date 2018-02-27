from django.db import models
from django.utils import timezone

# Create your models here.

class commite_member(models.Model) :
    name = models.CharField(max_length=100)
    number_on_list = models.CharField(max_length=3)


    def __str__self(self):
        return str(self.name)


class referat(models.Model):
    date = models.DateField(default=timezone.now)
    people = models.CharField(max_length=200)
    text = models.CharField(max_length=3000)



    def __str__self(self):
        return "Referat: "+str(self.date)