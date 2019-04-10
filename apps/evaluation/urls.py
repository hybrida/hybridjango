from django.conf.urls import url
from .views import *

app_name = 'evaluation'
urlpatterns = [
    url(r'^$', course_views , name='course_views'),
    url(r'^fag/(?P<pk>[0-9]+)/$', get_course, name='get_course'),
    url(r'^evaluation_form/$', get_evaluation_form, name='get_evaluation_form'),
]