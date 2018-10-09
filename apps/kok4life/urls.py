from django.conf.urls import url
from .views import *

app_name = 'kok'
urlpatterns = [
    url(r'^$', firstPage, name='firstPage')

    ]