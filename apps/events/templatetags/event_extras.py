from django import template

from apps.registration.models import get_graduation_year

register = template.Library()


@register.filter
def grade(value, arg):
    return value.filter(graduation_year=get_graduation_year(arg))
