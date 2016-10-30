from django import forms
from django.forms.models import model_to_dict, fields_for_model
from .models import Hybrid


class HybridForm(forms.ModelForm):
    def __init__(self, instance=None, *args, **kwargs):
        _fields = ('first_name', 'last_name', 'email',)
        _initial = model_to_dict(instance.user, _fields) if instance is not None else {}
        super(HybridForm, self).__init__(initial=_initial, instance=instance, *args, **kwargs)
        self.fields.update(fields_for_model(Hybrid, _fields))

    class Meta:
        model = Hybrid
        exclude = ('user', 'member',)

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.email = self.cleaned_data['email']
        u.save()
        profile = super(HybridForm, self).save(*args, **kwargs)
        return profile
