from django.db import models
from apps.registration.models import Hybrid

class Course(models.Model):

    name = models.CharField(max_length=255, blank=False, null=False)
    course_code = models.CharField(max_length=255, blank=False, null=False)
    grades_link = models.CharField(max_length=255)
    ntnu_link = models.CharField(max_length=255)
    average_score = models.DecimalField(decimal_places=2, max_digits=3,blank=True, null=True )



class Evaluation(models.Model):

    author = models.ForeignKey(Hybrid, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="evaluation")
    lecturer = models.CharField(
        max_length=255,
        blank=False,
        null=False)
    year = models.IntegerField(default=2010, max_length=4, blank=False, null=False)
    semester = models.IntegerField(blank=False, null=False) #1.-5.år
    season = models.CharField(max_length=255, blank=False, null=False) #Høst/vår
    title = models.CharField(max_length=255)
    evaluation_lecturer = models.TextField()
    evaluation_course = models.TextField()



