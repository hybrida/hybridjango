from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^fall$', views.index, name='evaluation_fall'),
    url(r'^spring$', views.spring, name='evaluation_spring'),
    url(r'^(?P<pk>[0-9]+)$', views.evaluation, name='evaluation'),

]