from django.core.validators import MaxValueValidator
from django.db import models
from apps.registration.models import Hybrid
from tinymce import HTMLField
from ..registration.models import Subject



class Evaluation(models.Model):

    author = models.ForeignKey(Hybrid, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="evaluation",
    verbose_name="Navn")
    lecturer = models.CharField(
        max_length=255,
        blank=False,
        null=False)

    year = models.IntegerField(default=2010, validators=[MaxValueValidator(3000)], blank=False, null=False, verbose_name="Året du tok faget")
    semester = models.IntegerField(blank=False, null=False, verbose_name="Semester faget ble gjennomført") #1.-5.år
    Seasons= (
        ('Høst', 'Høst'),
        ('Vår','Vår' )
    )
    season = models.CharField(choices=Seasons, max_length=255, blank=False, null=False, verbose_name="Årstid") #Høst/vår
    title = models.CharField(max_length=255, verbose_name="Tittel")
    evaluation_lecturer = HTMLField(verbose_name="Evaluering av foreleser")
    evaluation_course = HTMLField(verbose_name="Evaluering av faget")

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    Scores = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
    )
    score = models.IntegerField(choices=Scores, default=0, validators=[MaxValueValidator(5)])
    Profiles = (
        ('Geomatikk', 'Geomatikk'),
        ('Konstruksjonsteknikk', 'Konstruksjonsteknikk'),
        ('Marin teknikk', 'Marin teknikk'),
        ('Petroleumsfag', 'Petroleumsfag'),
        ('Produksjonsledelse', 'Produksjonsledelse'),
        ('Maskinteknikk', 'Maskinteknikk')

    )
    profile = models.CharField(choices=Profiles, max_length=250, blank=False, default="", null=True, verbose_name="Spesialisering")

    def __str__(self):
        return self.title
