from django.conf.urls import url

from . import views

app_name = 'kilt'
urlpatterns = [
    url(r'^$', views.index, name='info'),
    url(r'shop', views.bestilling, name='shop'),
    url(r'bestilling', views.shop, name='order'),
    url(r'admin', views.admin, name='admin'),
]