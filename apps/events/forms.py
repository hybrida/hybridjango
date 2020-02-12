from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, Submit, Button
from hybridjango.custom_layout_object import *
from hybridjango.mixins import BootstrapFormMixin
from .models import *


class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['event', 'text']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'type',
            'ingress',
            'text',  # TODO: Make this field a HTMLField in form
            'image',
            'event_start',
            'event_end',
            'weight',
            'location',
            'hidden',
            'news',
            'public',
            'signoff_close_on_signup_close',
            'signoff_close',
        ]
        widgets = {
            'ingress': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field] == self.fields['event_start'] or self.fields[field] == self.fields['event_end']:
                self.fields[field].widget.attrs.update({'class': 'form_datetime', 'autocomplete': 'off'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})


class MarkPunishmentForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = MarkPunishment
        exclude = [
            'rules',
            'delays',
            'duration',
        ]

    def __init__(self, *args, **kwargs):
        super(MarkPunishmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('goes_on_secondary'),
                Field('too_many_marks'),
                Field('signoff_close'),
                HTML("<br>"),
                Field('mark_on_late_signoff'),
                HTML("<br>"),
                Field('remove_on_too_many_marks'),
                HTML("<br>"),
                HTML("<br>"),
                Fieldset('Add delays',
                         Formset('delays')),
                HTML("<br>"),
                Fieldset('Add rules',
                         Formset('rules')),
                HTML("<br>"),
                Submit('submit', 'Lagre'),
                Button('back', "Tilbake", css_class='btn btn-default pull-right', onclick="goBack()"),
            )
        )


class RuleForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Rule
        exclude = [
            'punishment',
        ]


RuleFormSet = inlineformset_factory(
    MarkPunishment, Rule, form=RuleForm,
    fields=['rule'], extra=1, can_delete=True
)


class DelayForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Delay
        exclude = [
            'punishment',
        ]


DelayFormSet = inlineformset_factory(
    MarkPunishment, Delay, form=DelayForm,
    fields=['marks', 'minutes'], extra=1, can_delete=True
)
