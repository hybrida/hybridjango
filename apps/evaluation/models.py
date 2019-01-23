from django.db import models
from apps.registration.models import Hybrid

class Course(models.Model):

    name = models.CharField(max_length=255, blank=False, null=False)
    course_code = models.CharField(max_length=255, blank=False, null=False)
    grades_link = models.CharField(max_length=255)
    ntnu_link = models.CharField(max_length=255)


class Evaluation(models.Model):

    author = models.ForeignKey(Hybrid, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="evaluations")
    lecturer = models.CharField(
        max_length=255,
        blank=False,
        null=False)
    year = models.IntegerField(default=2010, max_length=4, blank=False, null=False)
    semester = models.IntegerField(blank=False, null=False)
    season = models.CharField(max_length=255, blank=False, null=False)
    title = models.CharField(max_length=255)
    evaluation_lecturer = models.TextField()
    evaluation_course = models.TextField()



