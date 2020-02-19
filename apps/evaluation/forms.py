from django import forms
from .models import Evaluation


class EvaluationForm(forms.ModelForm):

    class Meta:
        model = Evaluation
        fields = ['title', 'course', 'lecturer','year', 'season', 'semester' , 'evaluation_course', 'evaluation_lecturer', 'score']

    def __init__(self, *args, **kwargs):
        super(EvaluationForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['course'].widget.attrs.update({'class': 'form-control'})
        self.fields['lecturer'].widget.attrs.update({'class': 'form-control'})
        self.fields['year'].widget.attrs.update({'class': 'form-control'})
        self.fields['season'].widget.attrs.update({'class': 'form-control'})
        self.fields['semester'].widget.attrs.update({'class': 'form-control'})
        self.fields['evaluation_course'].widget.attrs.update({'class': 'form-control'})
        self.fields['evaluation_lecturer'].widget.attrs.update({'class': 'form-control'})
        self.fields['score'].widget.attrs.update({'class': 'form-control'})
