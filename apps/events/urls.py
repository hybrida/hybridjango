from django.conf.urls import url

from .views import EventList, EventView

urlpatterns = [
    url(r'^$', EventList.as_view(), name='events'),
    url(r'(?P<pk>[0-9]+)$', EventView.as_view(), name='event'),
]
