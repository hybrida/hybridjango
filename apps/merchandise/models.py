from django.db import models
from apps.registration.models import Hybrid
from django.utils import timezone
from tinymce import HTMLField
from django.urls import reverse


class Size(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):

    category_choices = (

    )
    sizes_choices = (
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL')
    )

    available_choices = (
        ('På lager', 'PÅ lager'),
        ('Under bestilling', 'Under bestilling'),
        ('Ikke tilgjengelig', 'Ikke tilgjengelig')
    )

    name = models.CharField(max_length=20)
    category = models.CharField(max_length=100, blank=True)
    description = HTMLField(blank=True)
    price = models.IntegerField(default=0)
    sizes = models.ManyToManyField(Size, blank=True)
    main_image = models.ImageField(blank=False)
    image1 = models.ImageField(blank=True)
    image2 = models.ImageField(blank=True)
    image3 = models.ImageField(blank=True)
    available = models.CharField(choices=available_choices, max_length=100, blank=True)

    def __str__(self):
        return self.name


class OrderElement(models.Model):
    product = models.ForeignKey(Product, related_name='order_element_product', on_delete=models.CASCADE)
    size = models.CharField(max_length=100)
    number = models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse('cartview')



class Cart(models.Model):
    user = models.ForeignKey(Hybrid, related_name='cart_user', on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderElement, blank=True)



class Order(models.Model):
    paid_choices = (
        ('Betalt', 'Betalt'),
        ('Ikke betalt', 'Ikke betalt'),
    )
    delivered_choices = (
        ('Hentet', 'Hentet'),
        ('Ikke hentet', 'Ikke hentet'),
    )
    user = models.ForeignKey(Hybrid, related_name='order_user', on_delete=models.CASCADE, blank=True)
    products = models.ManyToManyField(OrderElement, blank=True)
    timestamp = models.DateField(blank=False, default=timezone.now())
    sum = models.IntegerField(default=0)
    paid = models.CharField(choices=paid_choices, default='Ikke betalt', max_length=100)
    delivered = models.CharField(choices=delivered_choices, default='Ikke hentet', max_length=100)
    def get_products(self):
        return self.products.objects.all()
