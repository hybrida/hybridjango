from django.conf.urls import url
from .views import *

app_name = 'jobs'
urlpatterns = [
    url(r'^$', index, name='info'),
    url(r'^alle$', job_all, name='job_all'),
    url(r'^(?P<pk>[0-9]+)$', job_detail, name='job_detail'),
    url(r'^(?P<pk>[0-9]+)/endre/$', job_edit, name='job_edit'),
    url(r'ny', new_job, name='new'),
    url(r'admin', JobAdmin, name='admin'),
]