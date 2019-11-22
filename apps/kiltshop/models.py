from django.db import models
from apps.registration.models import Hybrid
from django.utils import timezone


class Product(models.Model):
    KILT = 'K'
    SPORRAN = 'S'
    EXTRA = 'E'
    type_choices = (
        (KILT, 'Kilt'),
        (SPORRAN, 'Sporran'),
        (EXTRA, 'Ekstra')
    )

    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='products', default='placeholder-event.png')
    type = models.CharField(max_length=1, choices=type_choices, default=KILT)
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
    period = models.ForeignKey(
        'OrderPeriod',
        related_name='orders',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "Ordre #{} for {}".format(self.pk, self.user.full_name)


class OrderPeriod(models.Model):
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def is_active(self):  # Checks if now is between start and end time.
        return self.start_time <= timezone.now() <= self.end_time

    def is_waiting(self):  # Checks if the start time is in the future
        return timezone.now() < self.start_time

    def __str__(self):
        return "{} - {}".format(self.start_time, self.end_time)


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    size = models.CharField(max_length=64, null=True)
