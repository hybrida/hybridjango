from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import RedirectView

from .views import *

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='home', permanent=False), name='event_list'),
    url(r'^liste$', EventList.as_view(), name='event_thumblist'),
    url(r'^kalenderinfo$', calendar_api, name='calendar_api'),
    url(r'^(?P<pk>[0-9]+)$', EventView.as_view(), name='event'),
    url(r'^(?P<pk>[0-9]+)/deltakere$',
        staff_member_required(EventView.as_view(template_name='events/participants.html', )),
        name='participants'),
    url(r'^(?P<pk>[0-9]+)/dashboard$',
        staff_member_required(EventView.as_view(template_name='events/event_dashboard.html')), name='dashboard'),
    url(r'^(?P<pk>[0-9]+)/dashboard/signed$', staff_member_required(signed), name='signed'),
    url(r'^(?P<pk>[0-9]+)/dashboard/attended$', staff_member_required(attended), name='attended'),
    url(r'^(?P<pk>[0-9]+)/dashboard/unattended$', staff_member_required(unattended), name='unattended'),
    url(r'^(?P<pk>[0-9]+)/csv$', staff_member_required(participants_csv), name='participants_csv'),
    url(r'^ny$', EventCreate.as_view(), name='new_event'),
    url(r'^(?P<pk>[0-9]+)/kommenter$', comment_event, name='comment_event'),
    url(r'^(?P<pk>[0-9]+)/slett_kommentar$', delete_comment_event, name='delete_comment_event'),
]
