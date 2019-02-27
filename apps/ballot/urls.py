from django.conf.urls import url

from .views import *

app_name = 'ballot'
urlpatterns = [
    url(r'^$', ballot, name='index'),
    url(r'^stem$', vote, name='vote'),
    url(r'^oversikt$', overview, name='overview'),
    url(r'^resultater$', get_results, name='results'),
    url(r'^valg$', get_choices, name='choices'),
    url(r'^forslag',suggestion, name='suggestion'),
]
