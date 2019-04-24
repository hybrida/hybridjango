from django import forms

from apps.bedkom.models import Company, Bedpress


class CompanyForm(forms.ModelForm):

    class Meta:
        fields = [
            'name',
            'responsible',
            'address',
            'info',
            'logo',
            'priority',
            'status',
        ]
        model = Company

    def __init__(self, *args, **kwargs):
            super(CompanyForm, self).__init__(*args, **kwargs)
            self.fields['name'].widget.attrs.update({'class': 'form-control'})
            self.fields['responsible'].widget.attrs.update({'class': 'form-control'})
            self.fields['address'].widget.attrs.update({'class': 'form-control'})
            self.fields['info'].widget.attrs.update({'class': 'form-control'})
            self.fields['logo'].widget.attrs.update({'class': 'form-control'})
            self.fields['priority'].widget.attrs.update({'class': 'form-control'})
            self.fields['status'].widget.attrs.update({'class': 'form-control'})

class BedpressForm(forms.ModelForm):
    ingress = forms.CharField(widget=forms.Textarea)

    class Meta:
        exclude = [
            'event.author',
            'event.participants',
            'event.timestamp',
        ]
        model = Bedpress