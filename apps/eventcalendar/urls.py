from django.conf.urls import url
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='eventcalendar/ecalendar.html'), name='ecalendar'),
]
