from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'sizes','main_image', 'image1', 'image2', 'image3', 'available']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['main_image'].widget.attrs.update({'class': 'form-control'})
        self.fields['image1'].widget.attrs.update({'class': 'form-control'})
        self.fields['image2'].widget.attrs.update({'class': 'form-control'})
        self.fields['image3'].widget.attrs.update({'class': 'form-control'})
        self.fields['available'].widget.attrs.update({'class': 'form-control'})