from django.conf.urls import url
from django.views.generic import TemplateView

from .views import *

app_name = 'gitlab'
urlpatterns = [
    url(r'^ny$', new, name='index'),
    url(r'^trenger-token$', TemplateView.as_view(template_name='gitlab/need_token.html'), name='need-token'),
]
