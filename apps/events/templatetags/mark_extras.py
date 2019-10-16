from django import template

from apps.events.models import Mark, Event


register = template.Library()


@register.filter
def num_marks(user):
    return Mark.num_marks(user)

@register.filter
def got_mark(user, event):
    if Mark.objects.filter(recipient=user, event=event).exists():
        return True
    return False

