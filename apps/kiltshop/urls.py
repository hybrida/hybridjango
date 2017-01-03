from django.conf.urls import url
from .views import *

app_name = 'kilt'
urlpatterns = [
    url(r'^$', index, name='info'),
    url(r'bestilling$', order, name='order'),
    url(r'shop$', shop, name='shop'),
    url(r'admin$', admin, name='admin'),
    url(r'admin/produkt$', admin_productoverview, name='admin_productoverview'),
    url(r'^(?P<pk>[0-9]+)/endre/$', product_edit, name='product_edit'),
    url(r'produkt/ny', product_new, name='product_new'),
]