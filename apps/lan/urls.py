from django.conf.urls import url

from .views import *

urlpatterns = [
        url(r'^create/$', CreateResult.as_view(template_name='lan/create_result.html'), name='create_result'),
        url(r'^list/$', ListResults.as_view(template_name='lan/list_results.html'), name='list_results'),
        url(r'^result/(?P<pk>[0-9]+)/delete$', DeleteResult.as_view(), name='result-delete'),

]