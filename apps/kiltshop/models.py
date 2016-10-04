from django.db import models

class kilt(models.Model):
    kilt_type= models.CharField(max_length=50) #Gutt,Jente,Jente_Mini,Jente_ultra_mini
    sporran = models.CharField(max_length=50) #Hvilken sporra, eks Black_leather, Celtic_targe osv...
    ekstra = models.CharField(max_length=250) #Må undersøke litt på hvordan denne skal gjøres.
    annet = models.CharField(max_length=500) #Evt andre kommentarer som skal tas hensyn til.