from django.conf.urls import url
from .views import *

app_name = 'evaluation'
urlpatterns = [
    url(r'^admin/$', admin, name='admin'),
]