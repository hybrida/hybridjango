from django.conf.urls import url
from .views import *

app_name = 'internside'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<pk>[0-9]+)/endre/upList', upList, name='upList'),
    url(r'^(?P<pk>[0-9]+)/endre/downList', downList, name='downList'),
    url(r'^(?P<pk>[0-9]+)/endre/bottom', bottom, name='bottom'),
    url(r'^(?P<pk>[0-9]+)/endre/edit', edit_todo, name='edit_todo'),
    url(r'^endre/prosjekt', AddProject, name='project-add'),
    url(r'êndre/referat, ', AddMeetingReport, name='meetingreport-add'),
    url(r'^(?P<pk>[0-9]+)/endre/top', top, name='top'),
    url(r'^dump', serve_data_dump, name='serve_data_dump'),
]
