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
    author = models.ForeignKey(Hybrid, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def sizes_as_list(self):
        return self.sizes.split(',')


    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(Hybrid, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductInfo')
    comment = models.CharField(max_length=200, blank=True)
    status = models.BooleanField(default=False)

    def get_orderinfo(self): #fetches the orderinfo an order lies in
        return OrderInfo.objects.filter(orders__id=self.pk).first()

    def __str__(self):
        return str("Ordre #"+str(self.pk)+" for "+self.user.first_name+" "+self.user.last_name)


class OrderInfo(models.Model):
    orders = models.ManyToManyField(Order, blank=True)
    startTime = models.DateTimeField(null=True, blank=True)
    endTime = models.DateTimeField(null=True, blank=True)

    def is_active(self): # Checks if now is between start and end time.
        if timezone.now() >= self.startTime:
            if timezone.now() <= self.endTime:
                return True
            else:
                return False
        else:
            return False

    def is_waiting(self):  # Checks if the start time is in the future
        if timezone.now() < self.startTime:
            return True
        else:
            return False

    def __str__(self):
        return str(str(self.startTime)+" - "+str(self.endTime))


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    size = models.CharField(max_length=64, null=True)
