from django import forms
from .models import EventComment


class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['event','text']