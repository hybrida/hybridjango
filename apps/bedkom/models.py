from django.db import models

# Create your models here.
class Bedrift:
    navn = None
    ansvarlig = None
    kontaktperson = None
    sisteKommentar = None

    def __init__(self, navn, ansvarlig, kontaktperson, sisteKommentar):
        self.navn = navn
        self.ansvarlig = ansvarlig
        self.kontaktperson = kontaktperson
        self.sisteKommentar = sisteKommentar