from django.conf.urls import url
from django.views.generic import RedirectView

from .views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='home', permanent=False), name='event_list'),
    url(r'^(?P<pk>[0-9]+)$', EventView.as_view(), name='event'),
    url(r'^ny$', EventCreate.as_view(), name='new_event'),
    url(r'^(?P<pk>[0-9]+)/comment$', comment_event, name='comment_event'),
]
