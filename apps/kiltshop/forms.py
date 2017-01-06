from django import forms
from .models import Product, Order, OrderInfo


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'type', 'image', 'link','sizes']


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['products', 'user']

class OrderInfoForm(forms.ModelForm):

    class Meta:
        model = OrderInfo
        fields = ['orders','startTime','endTime']