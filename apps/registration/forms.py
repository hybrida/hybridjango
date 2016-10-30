from django import forms
from .models import Hybrid


class HybridForm(forms.ModelForm):
    class Meta:
        model = Hybrid
        exclude = (
            'id',
            'password',
            'last_login',
            'is_superuser',
            'username',
            'is_staff',
            'is_active',
            'date_joined',
            'member',
        )
