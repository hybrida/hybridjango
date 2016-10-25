from django.contrib import admin
from .models import Product, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','type',)


class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ('products',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
