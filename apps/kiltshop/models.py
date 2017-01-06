from django.db import models
from apps.registration.models import Hybrid
from django.utils import timezone
import datetime

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
    sizes = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=1000, blank=True)
    author = models.ForeignKey(Hybrid)
    timestamp = models.DateTimeField(default=timezone.now)

    def sizes_as_list(self):
        return self.sizes.split(',')


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
    orders = models.ManyToManyField(Order, blank=True)
    startTime = models.DateTimeField(null=True, blank=True)
    endTime = models.DateTimeField(null=True, blank=True)

    def active_order(self):
        now = datetime.datetime.now()
        active_order = OrderInfo.objects.filter(endTime__gte=now).first()
        current_rorder = OrderInfo.objects.filter(pk=self.pk).first()
        if active_order==current_rorder:
            return True
        else:
            return False

    def __str__(self):
        return str(str(self.startTime)+" - "+str(self.endTime))


class ProductInfo(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order)
    number = models.IntegerField(default=1)
    size = models.CharField(max_length=64, null=True)
