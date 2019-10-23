from django import forms
from .models import Ridder, Honary_member


class RidderForm(forms.ModelForm):

    class Meta:
        model = Ridder
        fields = ('hybrid','finished','awarded','description')

        def __init__(self, *args, **kwargs):
            super(RidderForm, self).__init__(*args, **kwargs)
            self.fields['hybrid'].widget.attrs.update({'class': 'form-control'})
            self.fields['finished'].widget.attrs.update({'class': 'form-control'})
            self.fields['awarded'].widget.attrs.update({'class': 'form-control'})
            self.fields['description'].widget.attrs.update({'class': 'form-control'})