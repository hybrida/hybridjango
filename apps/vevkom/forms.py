from django import forms
from .models import Project


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
