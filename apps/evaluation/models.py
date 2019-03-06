from django.db import models
from apps.registration.models import Hybrid

class Course(models.Model):

    name = models.CharField(max_length=255, blank=False, null=False)
    course_code = models.CharField(max_length=255, blank=False, null=False)

    Specializations = (
        ('Geomatikk', 'Geomatikk'),
        ('Konstruksjonsteknikk', 'Konstruksjonsteknikk'),
        ('Marin teknikk', 'Marin teknikk'),
        ('Petroleumsfag', 'Petroleumsfag'),
        ('Produksjonsledelse', 'Produksjonsledelse'),
        ('Maskinteknikk', 'Maskinteknikk')
    )

    specialization = models.CharField(choices=Specializations, max_length=250, blank=True)
    grades_link = models.CharField(max_length=255)
    ntnu_link = models.CharField(max_length=255)
    average_score = models.DecimalField(decimal_places=2, max_digits=3, blank=True, null=True )

    Semesters = (
        ('Høst 3.', 'Høst 3.'),
        ('Vår 3.', 'Vår 3.'),
        ('Høst 4.', 'Høst 4.'),
        ('Vår 4.', 'Vår 4.'),
        ('Høst 5.', 'Høst 5.'),
        ('Vår 5.', 'Vår 5.')

    )
    semester = models.CharField(choices=Semesters, max_length=250, blank=False, default="")
    number_of_evaluations = models.IntegerField(default=0, blank=True)


class Evaluation(models.Model):

    author = models.ForeignKey(Hybrid, on_delete=models.CASCADE, blank=True, null=True)
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



