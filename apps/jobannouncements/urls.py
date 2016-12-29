from django.conf.urls import url
from .views import JobView

from . import views

app_name = 'kilt'
urlpatterns = [
    url(r'^$', views.index, name='info'),
    url(r'^(?P<pk>[0-9]+)$', JobView.as_view(), name='job'),
    url(r'ny', views.CreateJob, name='new'),
    url(r'admin', views.JobAdmin, name='admin'),
]