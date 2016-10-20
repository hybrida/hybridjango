from django import forms
from .models import EventComment, Event


class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['event', 'text']


class EventForm(forms.ModelForm):
    ingress = forms.CharField(widget=forms.Textarea)

    class Meta:
        exclude = [
            'author',
            'participants',
            'timestamp',
        ]
        model = Event
