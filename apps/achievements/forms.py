from django import forms

from .models import BadgeSuggestion, BadgeRequest, Badge


class BadgeSuggestionForm(forms.ModelForm):
    class Meta:
        model = BadgeSuggestion
        exclude = ['suggested_by']
        fields = ['name', 'description', 'award_to', 'image', 'scorepoints']
        labels = {
            'name': 'Navn',
            'description': 'Beskrivelse',
            'award_to': 'Tildeles',
            'image': 'Badge bilde'
        }

    def __init__(self, *args, **kwargs):
        super(BadgeSuggestionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


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
