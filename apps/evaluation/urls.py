from django.conf.urls import url
from django.urls import  path
from .views import *

app_name = 'evaluation'
urlpatterns = [
    path('', course_views , name='course_views'),
    path('fag/<int:pk>', get_course, name='get_course'),
    path('evaluation_form/', get_evaluation_form, name='get_evaluation_form'),
    path('search/', search, name='search')
]
