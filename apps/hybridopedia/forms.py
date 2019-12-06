from django import forms
from django.core.validators import RegexValidator

from hybridjango.mixins import BootstrapFormMixin
from .models import File

# This regex validator checks that the field is on the format <subject code> - <subject name>
# Subject code is 3 or 4 capital letters, then 4 digits
# Subject name is any number of words with any
subject_name_validator = RegexValidator(
    r'^[A-Z]{3,4}[0-9]{4}\s-([\s][\wæøåÆØÅ]+)+$',
    "Name is not on the correct format")

#name = forms.CharField(validators=[subject_name_validator], required=True)


class HybridopediaFileForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = File
        exclude = ['author']
