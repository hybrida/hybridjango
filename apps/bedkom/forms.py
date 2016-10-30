from django import forms

from apps.bedkom.models import Company


class CompanyForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)



    class Meta:
        fields = [
            'name',
            'responsible',
            'contact_person',
            'address',
            'description',
            'info',
            'notes',
            'priority',
            'status',
            'telephone',
        ]
        model = Company
