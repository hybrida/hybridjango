from django.conf.urls import url
from .views import *

app_name = 'evaluation'
urlpatterns = [
    url(r'^$', course_views , name='course_views'),
]