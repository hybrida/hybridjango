from django.conf.urls import url
from .views import EventList

urlpatterns = [
    url(r'^$', EventList.as_view(), name='events'),
]
