from django.conf.urls import url

from .views import *

app_name = 'rfid'
urlpatterns = [
    url(r'^(?P<pk>[0-9]+)$', AppearancesView.as_view(), name='rfid'),
    url(r'^(?P<pk>[0-9]+)/add$', add_appearance, name='add'),
]
