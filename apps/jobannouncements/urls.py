from django.conf.urls import url

from . import views

app_name = 'kilt'
urlpatterns = [
    url(r'^$', views.index, name='info'),
]