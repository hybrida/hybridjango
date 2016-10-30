from django.conf.urls import url
from django.contrib.auth.views import login, logout

from apps.registration import views

urlpatterns = [
    url(r'^$', views.redirect_to_profile, name='redirect_to_profile'),
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.complete_registration, name='complete_registration'),
    url(r'^(?P<slug>[\w.@+-]+)$', views.Profile.as_view(), name='profile'),
    url(r'^(?P<slug>[\w.@+-]+)/endre$', views.EditProfile.as_view(), name='edit_profile'),
]
