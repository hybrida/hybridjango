from django import forms
from django.utils import timezone

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


class GroupForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Hybrid
        fields = []

    hybrider = forms.ModelMultipleChoiceField(
        queryset=Hybrid.objects.filter(graduation_year__range=(timezone.now().year, timezone.now().year + 5)).order_by(
            'first_name'),
        widget=forms.SelectMultiple(attrs={
            'style': 'height:300px;',
        }), required=True)


class SubjectForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Subject
        exclude = ['author']
        fields = ['code', 'name']
