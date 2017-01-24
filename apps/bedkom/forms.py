from django import forms

from apps.bedkom.models import Company, Bedpress


class CompanyForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)



    class Meta:
        fields = [
            'name',
            'responsible',
            'address',
            'description',
            'info',
            'notes',
            'priority',
            'status',
        ]
        model = Company

class BedpressForm(forms.ModelForm):
    ingress = forms.CharField(widget=forms.Textarea)

    class Meta:
        exclude = [
            'event.author',
            'event.participants',
            'event.timestamp',
        ]
        model = Bedpress