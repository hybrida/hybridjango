from django import forms
from .models import EventComment, Event


class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['event', 'text']


class EventForm(forms.ModelForm):

    class Meta:
        exclude = [
            'author',
            'participants',
            'timestamp',
        ]
        widgets = {
            'ingress': forms.Textarea(attrs={'rows': 3}),
        }
        model = Event
