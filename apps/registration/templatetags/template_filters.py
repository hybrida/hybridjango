from django import template
from django.conf import settings
register = template.Library()


@register.filter
def get_if_waiting(value, user):
    if value.is_signed(user):
        return 'Påmeldt'
    elif value.is_waiting(user):
        return 'På venteliste'
