from django.conf.urls import url
from .views import *

app_name = 'kilt'
urlpatterns = [
    url(r'^$', index, name='info'),
    url(r'^bestilling/$', show_order, name='order'),
    url(r'^shop/$', shop, name='shop'),
    url(r'^admin/bestilling/$', period_overview, name='period_overview'),
    url(r'^admin/produkt/$', product_overview, name='product_overview'),
    url(r'^admin/produkt/(?P<pk>[0-9]+)/endre/$', product_edit, name='product_edit'),
    url(r'^admin/produkt/ny/$', product_new, name='product_new'),
    url(r'^admin/bestilling/(?P<pk>[0-9]+)/vis/$', orders_in_period, name='order_view'),
    url(r'admin/bestilling/ny/$', order_new, name='order_new'),
    url(r'^admin/bestilling/(?P<pk>[0-9]+)/endre/$', order_edit, name='order_edit'),
    url(r'^admin/bestilling/(?P<pk>[0-9]+)/excel$', download_period_as_excel, name='download_as_excel'),
]