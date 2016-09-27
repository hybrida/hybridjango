from django.db import models

# Create your models here.
class Bedrift:
    navn = None
    ansvarlig = None
    kontaktperson = None

    def __init__(self, navn, ansvarlig, kontaktperson):
        self.navn = navn
        self.ansvarlig = ansvarlig
        self.kontaktperson = kontaktperson