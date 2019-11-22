from django.conf.urls import url
from .views import *

app_name = 'kilt'
urlpatterns = [
    url(r'^$', index, name='info'),
    url(r'^bestilling/$', show_order, name='order'),
    url(r'^shop/$', shop, name='shop'),
    url(r'^admin/$', admin, name='admin'),
    url(r'^admin/bestilling/$', admin_orderoverview, name='admin_orderoverview'),
    url(r'^admin/produkt/$', admin_productoverview, name='admin_productoverview'),
    url(r'^admin/produkt/(?P<pk>[0-9]+)/endre/$', product_edit, name='product_edit'),
    url(r'^admin/produkt/ny/$', product_new, name='product_new'),
    url(r'^admin/bestilling/(?P<pk>[0-9]+)/vis/$', order_view, name='order_view'),
    url(r'admin/bestilling/ny/$', order_new, name='order_new'),
    url(r'^admin/bestilling/(?P<pk>[0-9]+)/endre/$', order_edit, name='order_edit'),
]