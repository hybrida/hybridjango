from django.conf.urls import url
from apps.accounts import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.redirect_to_profile, name='redirect_to_profile'),
    url(r'^login$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'(?P<pk>[0-9]+)$', views.Profile.as_view(), name='profile'),
    url(r'^register$', views.register, name='register'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.complete_registration, name='complete_registration'),
]
