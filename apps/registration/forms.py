from django import forms
from django.core.validators import RegexValidator

from hybridjango.mixins import BootstrapFormMixin
from .models import Hybrid, Subject


# This regex validator checks that the field is on the format <subject code> - <subject name>
# Subject code is 3 or 4 capital letters, then 4 digits
# Subject name is any number of words with any
subject_name_validator = RegexValidator(
    r'^[A-Z]{3,4}[0-9]{4}\s-([\s][\wæøåÆØÅ]+)+$',
    "Name is not on the correct format")


class HybridForm(forms.ModelForm):
    class Meta:
        model = Hybrid
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'title',
            'email',
            'image',
            'graduation_year',
            'specialization',
            'gender',
            'food_preferences',
            'card_key',
        )


class SubjectForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Subject
        exclude = ['author']
        fields = ['code', 'name']

    name = forms.CharField(validators=[subject_name_validator], required=True)
