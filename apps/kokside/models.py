from django.db import models

# Create your models here.
class kok(models.Model):
    kokfil = models.FileField(upload_to='pdf/referat')
    description = models.CharField(max_length=50, blank=True)
    number = models.CharField(max_length=4, blank=False)


    def __str__(self):
        return "Referat: "