from django import forms


class TodoForm(forms.Form):
    project_name = forms.CharField(label="project_name",max_length=150)
    description = forms.CharField(label="description", max_length=1000)
    priority = forms.CharField(choices="Choices", max_length=20)
    status = forms.CharField(choices="Choices_status", max_length=20)
    project_members = forms.CharField(max_length=500, blank=True)

    Choices = (
        ('høy', 'høy'),
        ('middels', 'middels'),
        ('lav', 'lav'),
    )

    Choices_status = (
        ('ferdig', 'ferdig'),
        ('påbegynt','påbegynt'),
        ('ikke påbegynt', 'ikke påbegynt'),
    )