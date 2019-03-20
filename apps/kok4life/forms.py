from django import forms
from .models import Subject, File


class KokFileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ['author']


class KokSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
