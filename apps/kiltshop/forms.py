from django import forms
from .models import Product, Order, OrderPeriod


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'type', 'image', 'link', 'sizes']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['products', 'user']


class OrderPeriodForm(forms.ModelForm):
    class Meta:
        model = OrderPeriod
        fields = ['startTime', 'endTime']
