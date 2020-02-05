import os
from datetime import timedelta

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse
from django.utils import timezone


def get_graduation_year(grade):
    return five_years() - int(grade)


def five_years():
    return (timezone.now() + timedelta(weeks=26)).year + 5


def user_folder(instance, filename):
    return os.path.join('users', instance.username, filename)


class Specialization(models.Model):
    name = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True, blank=False, null=False)

    def __str__(self):
        return self.name


class CaseInsensitiveUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class Hybrid(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Mellomnavn')
    member = models.BooleanField(default=False, verbose_name='Medlem')
    graduation_year = models.IntegerField(default=five_years, verbose_name='Avgangsår')
    image = models.ImageField(upload_to=user_folder, default='placeholder-profile.jpg', verbose_name='Bilde')
    gender = models.CharField(max_length=1, blank=False, choices=(('M', 'Mann'), ('F', 'Dame'), ('U', 'Ukjent')),
                              verbose_name='Kjønn', default='U')
    specialization = models.ForeignKey(Specialization, null=True, on_delete=models.SET_NULL,
                                       verbose_name='Spesialisering', limit_choices_to={'active': True})
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Fødselsår')
    title = models.CharField(max_length=150, blank=True, default='Hybrid', verbose_name='Tittel')
    food_preferences = models.CharField(max_length=150, blank=True, verbose_name='Allergier og matpreferanser')
    card_key = models.CharField(max_length=10, null=True, blank=True, unique=True, verbose_name='NTNU-kortkode')
    accepted_conditions = models.BooleanField(default=False)

    objects = CaseInsensitiveUserManager()

    def get_full_name(self):
        if self.middle_name:
            first_name = self.first_name + ' ' + self.middle_name
        else:
            first_name = self.first_name
        if first_name == "" and self.last_name == "":
            return self.username
        return first_name + ' ' + self.last_name

    full_name = property(get_full_name)

    def get_grade(self):
        return five_years() - self.graduation_year

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.username})


class RecoveryMail(models.Model):
    hybrid = models.ForeignKey(Hybrid, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return "{}_{}".format(self.hybrid, self.timestamp)


class ContactPerson(models.Model):
    """
    A class for users to be presented somewhere on the site as contact persons
    E.g. the board, KTV, ITV
    """

    def __getattr__(self, item):
        """
        When calling foo.bar (getting attribute bar on object foo) in python,
        the actual call is foo.__getattribute__('bar').
        If that fails, foo.__getattr__('bar') is attempted.

        Here, we override __getattr__ with a call to user.__getattribute__.
        This means that attributes in the user object that do not exist here can be gotten directly,
        e.g. calling contact_person_object.first_name will return contact_person_object.user.first_name.
        """
        return self.user.__getattribute__(item)

    user = models.ForeignKey(Hybrid, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=128, null=False, blank=False)
    # a unique name for getting objects, even when title is the same
    search_name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)


class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Fagnavn")
    code = models.CharField(max_length=10, unique=True, null=False, blank=False, verbose_name="Fagkode")

    Years = (
        ('First', 'Første'),
        ('Second', 'Andre'),
        ('Third', 'Tredje'),
        ('Fourth', 'Fjerde'),
        ('Fifth', 'Femte'),
        ('Third-Fifth', 'Tredje til Femte'),
    )
    Semesters = (
        ('Autumn', 'Høst'),
        ('Spring', 'Vår'),
        ('Both', 'Begge'),
    )
    Specializations = (
        ('Geomatikk', 'Geomatikk'),
        ('Konstruksjonsteknikk', 'Konstruksjonsteknikk'),
        ('Marin teknikk', 'Marin teknikk'),
        ('Petroleumsfag', 'Petroleumsfag'),
        ('Produksjonsledelse', 'Produksjonsledelse'),
        ('Maskinteknikk', 'Maskinteknikk')
    )

    year = models.CharField(choices=Years, max_length=250, blank=False, default="", verbose_name="Trinn")
    semester = models.CharField(choices=Semesters, max_length=250, blank=False, default="", verbose_name="Semester")
    specialization = models.CharField(choices=Specializations, max_length=250, blank=True, verbose_name="Spesialisering")

    # Used in course evaluation
    grades_link = models.CharField(max_length=255, blank=True)
    ntnu_link = models.CharField(max_length=255, blank=True)
    average_score = models.DecimalField(decimal_places=2, max_digits=3, blank=True, null=True)
    number_of_evaluations = models.IntegerField(default=0, blank=True)

    author = models.ForeignKey(Hybrid, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

