from django import forms
from .models import Subject, File


class HybridopediaFileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ['author']
        fields = ['name', 'file', 'subject']

    def __init__(self, *args, **kwargs):
        super(HybridopediaFileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})


class HybridopediaSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(HybridopediaSubjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
