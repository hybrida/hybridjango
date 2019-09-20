from django.conf.urls import url
from .views import *

app_name = 'hybridopedia'
urlpatterns = [
    url(r'^$', firstPage, name='firstPage'),
    url(r'^fag/(?P<pk>[0-9]+)$', filePage, name='filePage'),
    url(r'^fileform$', fileForm, name='fileForm'),
    url(r'^subjectform$', subjectForm, name='subjectForm'),
]
