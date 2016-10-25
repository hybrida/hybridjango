from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    kilt='K'
    sporran='S'
    extra='E'

    type_choices = (
        (kilt, 'Kilt'),
        (sporran, 'Sporran'),
        (extra, 'Ekstra')
    )


    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='products', default='placeholder-event.png')
    type = models.CharField(max_length=1, choices=type_choices, default=kilt)

    def __str__(self):
        return self.name


class Order(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.user)