from django import forms
from .models import Ridder, Honary_member


class RidderForm(forms.ModelForm):

    class Meta:
        model = Ridder
        fields = ('name','finished','awarded','description')