from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='products', default='placeholder-event.png')

    def __str__(self):
        return self.name


class Order(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User)