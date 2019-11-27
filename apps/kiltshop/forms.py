from django import forms
from django.utils import timezone
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

    def clean_end_time(self):
        data = self.cleaned_data['end_time']
        now = timezone.now()
        # other periods with end_time in the future
        future_periods = OrderPeriod.objects.filter(end_time__gte=now).exclude(pk=self.instance.pk)

        if data >= now and future_periods.exists():
            raise forms.ValidationError('Det finnes allerede en periode frem i tid.')

        return data

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError('Starten må være før slutten.')
