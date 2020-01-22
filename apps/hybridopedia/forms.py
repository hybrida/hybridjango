from django import forms

from hybridjango.mixins import BootstrapFormMixin
from .models import File


class HybridopediaFileForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = File
        exclude = ['author']
        fields = ['name', 'file', 'subject']
