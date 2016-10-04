from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='info'),
    url(r'shop', views.bestilling, name='shop'),
    url(r'bestilling', views.shop, name='bestilling'),
    url(r'admin', views.admin, name='admin'),
]