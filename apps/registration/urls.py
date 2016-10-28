from django.conf.urls import url
from django.contrib.auth.views import *

from apps.registration import views

urlpatterns = [
    url(r'^$', views.redirect_to_profile, name='redirect_to_profile'),
    url(r'^logg_inn$', login, name='login'),
    url(r'^logg_ut$', logout, name='logout'),
    url(r'^endre_passord/$', password_change, name='password_change'),
    url(r'^endre_passord/ferdig/$', password_change_done,
        name='password_change_done'),
    url(r'^gjenopprett/$', password_reset, name='password_reset'),
    url(r'^gjenopprett/ferdig/$', password_reset_done,
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>0-9A-Za-z_\-+)/(?P<token>0-9A-Za-z1,13-0-9A-Za-z1,20)/$', password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^reset/ferdig/$', password_reset_complete,
        name='password_reset_complete'),
    url(r'(?P<pk>[0-9]+)$', views.Profile.as_view(), name='profile'),
]
