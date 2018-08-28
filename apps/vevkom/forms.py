from django import forms
from .models import Project, MeetingReport


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'responsible', 'description', 'status', 'priority']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['responsible'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['priority'].widget.attrs.update({'class': 'form-control'})

class MeetingReportForm(forms.ModelForm):

    class Meta:
        model = MeetingReport
        fields = ['date', 'tilstede', 'text']

    def __init__(self, *args, **kwargs):
        super(MeetingReportForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['tilstede'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
