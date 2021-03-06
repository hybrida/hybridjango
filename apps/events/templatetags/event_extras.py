from datetime import datetime

from django import template
from django.conf import settings

from apps.registration.models import get_graduation_year

register = template.Library()


@register.filter
def readable_gender(value):
    if value == 'M':
        return 'Menn'
    elif value == 'F':
        return 'Damer'
    return 'Andre'


# settings value
@register.simple_tag
def absolute_uploads_url(relative_url):
    return "{}/uploads/{}".format(getattr(settings, "SERVER_URL", ""), relative_url)


@register.filter
def grade_list(value, arg):
    return [hybrid for hybrid in value if hybrid.graduation_year == get_graduation_year(arg)]


TIMEUNTIL_CHUNKS = (
    (60 * 60 * 24 * 365, '1 år', '%d år'),
    (60 * 60 * 24 * 30, '1 måned', '%d måneder'),
    (60 * 60 * 24 * 7, '1 uke', '%d uker'),
    (60 * 60 * 24, '1 dag', '%d dager'),
    (60 * 60, '1 time', '%d timer'),
    (60, '1 minutt', '%d minutter')
)


@register.filter
def timeuntil2(d):
    now = datetime.now(d.tzinfo)
    delta = d - now

    until = delta.days * 24 * 60 * 60 + delta.seconds
    if until <= 0:
        return '0 minutter'
    for i, (seconds, singular, plural) in enumerate(TIMEUNTIL_CHUNKS):
        count = until // seconds
        if count != 0:
            break
    result = singular if count == 1 else plural % count
    if i + 1 < len(TIMEUNTIL_CHUNKS):
        seconds2, singular2, plural2 = TIMEUNTIL_CHUNKS[i + 1]
        count2 = (until - (seconds * count)) // seconds2
        if count2 != 0:
            result += ' og ' + (singular2 if count2 == 1 else plural2 % count2)
    return result
