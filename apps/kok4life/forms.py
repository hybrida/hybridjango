from django import forms

from .models import Subject, File

class KokfForm(forms.ModelForm):

    class meta:
        model = File
        fields = [
            'navn'
            'file'
        ]

class KoksForm(forms.ModelForm):

    class meta:
        model = Subject
        fields = ['navn']


