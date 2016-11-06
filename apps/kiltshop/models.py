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
    status = models.BooleanField(default=False)

    def __str__(self):
        return str("Bestilling  : "+self.user.first_name+" "+self.user.middle_name+" "+self.user.last_name)


class OrderInfo(models.Model):
    orders = models.ManyToManyField(Order, null=True, blank=True)
    startTime = models.DateTimeField(null=True, blank=True)
    endTime = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(str(self.startTime)+" - "+str(self.endTime)+" ("+str(self.status)+")")


class ProductInfo(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order)
    number = models.IntegerField(default=1,)
    size = models.CharField(max_length=64, blank=True)

    class Meta():
        auto_created = True