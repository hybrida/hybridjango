from django import forms
from .models import BadgeForslag


class BadgeForslagForm(forms.ModelForm):

    class Meta:
        model = BadgeForslag
        exclude = ['profil']
        fields = ['navn', 'beskrivelse', 'tildeles', 'badge_bilde', 'scorepoints']

    def __init__(self, *args, **kwargs):
        super(BadgeForslagForm, self).__init__(*args, **kwargs)
        self.fields['navn'].widget.attrs.update({'class': 'form-control'})
        self.fields['beskrivelse'].widget.attrs.update({'class': 'form-control'})
        self.fields['tildeles'].widget.attrs.update({'class': 'form-control'})
        self.fields['badge_bilde'].widget.attrs.update({'class': 'form-control'})
        self.fields['scorepoints'].widget.attrs.update({'class': 'form-control'})
