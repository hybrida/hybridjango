from django.db import models
from apps.registration.models import Hybrid
from apps.registration.models import Specialization
import datetime


class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=500, null=True)
    semester = models.CharField(max_length=4, null=True)

    def __str__(self):
        return self.code + " - " + self.name


class Evaluation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    workload = models.IntegerField(default=1)
    difficulty = models.IntegerField(default=1)
    learn = models.CharField(max_length=2500, null=True)
    structure = models.CharField(max_length=2500, null=True)
    useful = models.CharField(max_length=2500, null=True)
    comment = models.CharField(max_length=2500, null=True)
    grade = models.IntegerField(default=3)
    year = models.IntegerField(default=2017)
    anonymous = models.BooleanField(default=False)
    specializaion = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    user = models.ForeignKey(Hybrid, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.name + ": " + str(self.pk)
