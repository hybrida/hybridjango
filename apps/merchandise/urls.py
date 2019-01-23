from  django.conf.urls import url
from django.conf import settings
from .views import shop, product_page, AddItemToCart, CartVeiw, OrderCart, OrderOverview, DeleteOrderElement, \
    order_overview_product, order_status_change, DeleteOrder, AddProduct
"""
COMMENT BACK IN TO DEPLOY
urlpatterns =[
    url(r'^$', shop, name='shop'),
    url(r'^produkt/(?P<pk>[0-9]+)/$', product_page, name='product_page'),
    url(r'^cart/add/(?P<pk>[0-9]+)/$', AddItemToCart, name='add_to_cart'),
    url(r'^cart/$', CartVeiw, name='cartview'),
    url(r'^cart/order/$', OrderCart, name='order_cart'),
    url(r'order/overview/$', OrderOverview, name='order_overview'),
    url(r'^element/(?P<pk>[0-9]+)/delete/$', DeleteOrderElement.as_view(), name='delete_element'),
    url(r'^order/overview/(?P<pk>[0-9]+)', order_overview_product, name='order_overview_product'),
    url(r'^order/deliveredpaid//(?P<pk>[0-9]+)', order_status_change, name='order_status_change'),
    url(r'^order/(?P<pk>[0-9]+)/delete/$', DeleteOrder.as_view(), name='delete_order'),
    url(r'^product/add/$', AddProduct.as_view(), name='add_product')
]
"""