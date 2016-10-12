from django.conf.urls import url
from apps.bedkom import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^bedrift/(?P<company_id>[0-9]+)$', views.bedrift, name='bedrift'),
    url(r'^(?P<company_pk>[0-9]+)/kommenter/$', views.comment, name='comment'),
    url(r'^bedrift/bedpress/(?P<bedpress_id>[0-9]+)$', views.bedpress, name='bedpress')
]
