from django.conf.urls import url
from django.urls import path
from .views import *


urlpatterns = [
            url(r'^hybridaFK', hybridaFK, name='hybridafk'),
        ]