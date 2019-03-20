from django import forms

from .models import Result

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ("user", "time")
    
    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = (
                self.fields['user'].queryset.order_by('username')) 
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
