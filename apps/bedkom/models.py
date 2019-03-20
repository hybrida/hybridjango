
from django.db import models
from django.utils import timezone
from django.urls import reverse
from apps.events.models import Event
from apps.registration.models import Hybrid, Specialization


class Contact_person(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50, default="")
    job = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Kontaktperson'
        verbose_name_plural = 'Kontaktpersoner'


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Navn')
    responsible = models.ForeignKey(Hybrid, null=True, blank=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=150, null=True, blank=True)
    info = models.CharField(max_length=300, null=True, blank=True,
                            help_text='Hvem er bedriften, hva gjør de og hvilke fagområder er de involvert i?')
    logo = models.ImageField(upload_to='companies', default='placeholder-logo.png')
    contact_person = models.ForeignKey(Contact_person, blank=True, null=True, on_delete=models.CASCADE)
    relevant_spesializations = models.ManyToManyField(Specialization,blank=True)

    CHOICES_STATUS = (
        ('Booket', 'Booket'),
        ('Opprettet kontakt', 'Opprettet kontakt'),
        ('Takket nei', 'Takket nei'),
        ('Ikke kontaktet', 'Ikke kontaktet'),
        ('Svarer ikke', 'Svarer ikke'),

    )

    CHOICES_PRIORITY = (
        ('Høy', 'Høy'),
        ('Middels', 'Middels'),
        ('Lav', 'Lav')
    )

    status = models.CharField(choices=CHOICES_STATUS, max_length=20)
    priority = models.CharField(choices=CHOICES_PRIORITY, max_length=20, null=True)

    def get_absolute_url(self):
        return reverse('bedrift', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Bedrift'
        verbose_name_plural = 'Bedrifter'


class Bedpress(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    verbose_name = "Bedriftspresentasjoner"

    def __str__(self):
        return str(self.company.name) + " den " + str(self.event)

    class Meta:
        verbose_name = 'Bedriftspresentasjon'
        verbose_name_plural = 'Bedriftspresentasjoner'


class CompanyComment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    author = models.ForeignKey(Hybrid, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    text = models.TextField()

    def __str__(self):
        return str(
            str(self.author.first_name) + " " + str(self.author.last_name) + " in " + str(self.company) + ": " + str(
                self.text))


class MeetingReport(models.Model):
    report = models.FileField(upload_to='pdf/referat')
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "Referat: "+str(self.date)

    def get_absolute_url(self):
        return reverse('bkreports')

