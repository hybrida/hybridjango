from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import Product, Order, ProductInfo, OrderInfo


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)


class ProductInfoInline(admin.TabularInline):
    model = ProductInfo
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ('products',)
    inlines = (ProductInfoInline,)

    formfield_overrides = {
        models.CharField: {'widget': Textarea(
            attrs={'rows': 20,
                   'cols': 60,
                   'style': 'height: 10em;'})},
    }

class OrderInfoAdmin(admin.ModelAdmin):
    filter_horizontal = ('orders',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)

