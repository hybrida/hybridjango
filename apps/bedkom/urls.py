from django.conf.urls import url
from apps.bedkom import views

urlpatterns = [
    url(r'^$', views.index),
]