from django.conf.urls import url
from .views import index, upList, downList, bottom, edit_todo, AddProject

app_name = 'internside'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<pk>[0-9]+)/endre/upList', upList, name='upList'),
    url(r'^(?P<pk>[0-9]+)/endre/downList', downList, name='downList'),
    url(r'^(?P<pk>[0-9]+)/endre/bottom', bottom, name='bottom'),
    url(r'^(?P<pk>[0-9]+)/endre/edit', edit_todo, name='edit_todo'),
    url(r'^endre/prosjekt', AddProject.as_view(), name='project-add')
]
