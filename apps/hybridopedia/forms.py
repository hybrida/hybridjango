from django import forms
from .models import Subject, File


class KokFileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ['author']
        fields = ['name', 'file', 'subject']
    def __init__(self, *args, **kwargs):
        super(KokFileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})


class KokSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
    def __init__(self, *args, **kwargs):
        super(KokSubjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})