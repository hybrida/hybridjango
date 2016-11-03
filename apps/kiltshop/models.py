from django.db import models
from apps.registration.models import Hybrid


class Product(models.Model):
    kilt = 'K'
    sporran = 'S'
    extra = 'E'

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
    user = models.ForeignKey(Hybrid)
    products = models.ManyToManyField(Product, through='ProductInfo')
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str("Bestilling  : "+self.user.first_name+" "+self.user.middle_name+" "+self.user.last_name)


class ProductInfo(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order)
    number = models.IntegerField(default=1,)
    size = models.CharField(max_length=64, blank=True)

    class Meta():
        auto_created = True