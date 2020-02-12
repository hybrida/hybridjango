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


class HybridModelField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return '{} ({})'.format(obj.full_name, obj.username)


class GroupForm(forms.Form):
    class Meta:
        fields = ['hybrids']

    hybrids = HybridModelField(
        queryset=Hybrid.objects.filter(graduation_year__range=(timezone.now().year, timezone.now().year + 5)).order_by(
            'first_name'),
        widget=forms.SelectMultiple(attrs={
            'style': 'height:300px; width:100%',
            'id': 'hybrids',
        }), required=True)

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['hybrids'].widget.attrs.update({'class': 'form-control'})


class SubjectForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Subject
        exclude = ['author']
        fields = ['code', 'name', 'year', 'semester', 'specialization']
