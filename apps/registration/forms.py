from django import forms

from hybridjango.mixins import BootstrapFormMixin
from .models import Hybrid, Subject


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
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
