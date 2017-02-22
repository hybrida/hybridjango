from django.conf.urls import url
from .views import *

app_name = 'jobs'
urlpatterns = [
    url(r'^$', index, name='info'),
    url(r'^tidligere$', job_previous, name='job_previous'),
    url(r'^(?P<pk>[0-9]+)$', job_detail, name='job_detail'),
    url(r'^(?P<pk>[0-9]+)/endre/$', job_edit, name='job_edit'),
    url(r'nybedrift', new_job, name='new'),
    url(r'admin', JobAdmin, name='admin'),
]