from django.conf.urls import url
from .views import *

app_name = 'hybridopedia'
urlpatterns = [
    url(r'^$', first_page, name='firstPage'),
    url(r'^fag/(?P<pk>[0-9]+)$', file_page, name='filePage'),
    url(r'^fileform$', file_form, name='fileForm'),
    url(r'^subjectform$', subject_form, name='subjectForm'),
]
