from django import forms
from hybridjango.mixins import BootstrapFormMixin
from .models import CommiteApplication, Application, Statute, Updatek


class CommiteApplicationForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = CommiteApplication
        exclude = ['navn']
        fields = ['prioritet_1', 'prioritet_2', 'prioritet_3', 'prioritet_4', 'kommentar']


class ApplicationForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Application
        exclude = ['granted', 'comment']
        fields = ['navn', 'beskrivelse']


class StatuteForm(forms.ModelForm):
    class Meta:
        model = Statute
        fields = ['statute', 'date']


class UpdatekForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Updatek
        fields = ['frontpage', 'pdf', 'school_year', 'edition']
