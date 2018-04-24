from django import forms
from .models import ComApplication


class CommiteApplicationForm(forms.ModelForm):

    class Meta:
        model = ComApplication
        exclude = ['navn']
        fields = ['prioritet_1', 'prioritet_2', 'prioritet_3', 'prioritet_4', 'kommentar']

    def __init__(self, *args, **kwargs):
        super(CommiteApplicationForm, self).__init__(*args, **kwargs)
        self.fields['prioritet_1'].widget.attrs.update({'class': 'form-control'})
        self.fields['prioritet_2'].widget.attrs.update({'class': 'form-control'})
        self.fields['prioritet_3'].widget.attrs.update({'class': 'form-control'})
        self.fields['prioritet_4'].widget.attrs.update({'class': 'form-control'})
        self.fields['kommentar'].widget.attrs.update({'class': 'form-control'})

