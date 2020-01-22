from django.contrib import admin
from .models import Product,Size, OrderElement, Cart, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(OrderElement)
admin.site.register(Cart)
admin.site.register(Order)
