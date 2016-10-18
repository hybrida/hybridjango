from django.conf.urls import url

from . import views

app_name = 'kilt'
urlpatterns = [
    url(r'^$', views.index, name='info'),
    url(r'^info2', views.info2, name='info2'),
    url(r'bestilling', views.bestilling, name='order'),
    url(r'shop', views.shop, name='shop'),
    url(r'admin', views.admin, name='admin')
]