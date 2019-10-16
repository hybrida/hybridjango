from django import forms
from django.core.validators import RegexValidator
from .models import Subject, File

# This regex validator checks that the field is on the format <subject code> - <subject name>
# Subject code is 3 or 4 capital letters, then 4 digits
# Subject name is any number of words with any
subject_name_validator = RegexValidator(
    r'^[A-Z]{3,4}[0-9]{4}\s-([\s][\wæøåÆØÅ]+)+$',
    "Name is not on the correct format")


class HybridopediaFileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        super(HybridopediaFileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})


class HybridopediaSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ['author']

    name = forms.CharField(validators=[subject_name_validator], required=True)

    def __init__(self, *args, **kwargs):
        super(HybridopediaSubjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
