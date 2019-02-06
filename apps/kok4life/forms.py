from django import forms
from .models import Subject, File


class KokfForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ['author']


class KoksForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


