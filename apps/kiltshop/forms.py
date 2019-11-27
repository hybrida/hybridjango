from django import forms
from .models import Product, Order, OrderPeriod
from hybridjango.mixins import BootstrapFormMixin


class ProductForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Product
        fields = ['name', 'type', 'image', 'link', 'sizes']


class OrderForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Order
        fields = ['products', 'user']


class OrderPeriodForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = OrderPeriod
        fields = ['start_time', 'end_time']
