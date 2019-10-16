from django import template

from apps.events.models import Mark

register = template.Library()


@register.filter
def num_marks(user):
    return Mark.num_marks(user)
