from django.conf.urls import url
from .views import index

urlpatterns = [
    url(r'^$', index, name='internside'),
    url(r'^list/$', list, name='list')


]