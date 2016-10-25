from django import template
from apps.events.models import Event
from apps.accounts.models import get_graduation_year

register = template.Library()


@register.filter
def grade(value, arg):
    return value.filter(hybrid__graduation_year=get_graduation_year(arg))
