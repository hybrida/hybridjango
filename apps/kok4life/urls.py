from django.conf.urls import url
from .views import *

app_name = 'kok'
urlpatterns = [
    url(r'^firstpage$', firstPage, name='firstPage'),
    url(r'^fag/(?P<pk>[0-9]+)$', filePage, name='filePage')
    ]