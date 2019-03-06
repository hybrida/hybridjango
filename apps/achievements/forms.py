from django import forms

from .models import BadgeForslag, BadgeRequest, Badge


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


class BadgeRequestForm(forms.ModelForm):
    class Meta:
        model = BadgeRequest
        exclude = ['user', 'badge', 'status']
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(BadgeRequestForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})


class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        exclude = ['user']
        fields = ['name', 'description', 'badge_image', 'scorepoints']

    def __init__(self, *args, **kwargs):
        super(BadgeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
