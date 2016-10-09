from django.conf.urls import url

from .views import EventList, EventView, EventCreate, EventEdit, EventDelete, join_event, leave_event

urlpatterns = [
    url(r'^$', EventList.as_view(), name='event_list'),
    url(r'^(?P<pk>[0-9]+)$', EventView.as_view(), name='event'),
    url(r'^ny$', EventCreate.as_view(), name='new_event'),
    url(r'^(?P<pk>[0-9]+)/endre$', EventEdit.as_view(), name='edit_event'),
    url(r'^(?P<pk>[0-9]+)/slett$', EventDelete.as_view(), name='delete_event'),
    url(r'^(?P<pk>[0-9]+)/meldpaa$', join_event, name='join_event'),
    url(r'^(?P<pk>[0-9]+)/meldav$', leave_event, name='leave_event'),
]
