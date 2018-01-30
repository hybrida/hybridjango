from django import forms

from .models import Hybrid


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
