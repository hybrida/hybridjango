from django.conf.urls import url
from apps.bedkom import views
from apps.bedkom.views import BedriftEndre, BedriftLag

urlpatterns = [
    url(r'^$', views.index),
    url(r'^bedrift/(?P<pk>[0-9]+)$', views.bedrift, name='bedrift'),
    url(r'^(?P<pk>[0-9]+)/kommenter/$', views.comment, name='comment'),
    url(r'^bedrift/bedpress/(?P<pk>[0-9]+)$', views.bedpress, name='bedpress'),
    url(r'^bedrift/(?P<pk>[0-9]+)/endre$', BedriftEndre.as_view(), name='endre_bedrift'),
    url(r'^nybedrift/', BedriftLag.as_view(), name='lag_bedrift'),

]
