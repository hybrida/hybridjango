from django import forms
from .models import CommiteApplication, Application


class CommiteApplicationForm(forms.ModelForm):

    class Meta:
        model = CommiteApplication
        exclude = ['navn']
        fields = ['prioritet_1', 'prioritet_2', 'prioritet_3', 'prioritet_4', 'kommentar']

    def __init__(self, *args, **kwargs):
        super(CommiteApplicationForm, self).__init__(*args, **kwargs)
        self.fields['prioritet_1'].widget.attrs.update({'class': 'form-control'})
        self.fields['prioritet_2'].widget.attrs.update({'class': 'form-control'})
        self.fields['prioritet_3'].widget.attrs.update({'class': 'form-control'})
        self.fields['prioritet_4'].widget.attrs.update({'class': 'form-control'})
        self.fields['kommentar'].widget.attrs.update({'class': 'form-control'})

class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        exclude = ['granted', 'comment']
        fields = ['navn', 'beskrivelse']

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['navn'].widget.attrs.update({'class': 'form-control'})
        self.fields['beskrivelse'].widget.attrs.update({'class': 'form-control'})
