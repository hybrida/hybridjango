from django.urls import path
from .views import *
from django.views.generic.base import TemplateView

app_name = 'lan'
urlpatterns = [
    path('test/', TemplateView.as_view(template_name='lan/index.html'))
]