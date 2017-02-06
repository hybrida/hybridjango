from django.conf.urls import url
from apps.bedkom import views
from apps.bedkom.views import comment_company, bedpress_company_comment

urlpatterns = [
    url(r'^$', views.index, name='bedkom'),
    url(r'^bedrift/(?P<pk>[0-9]+)$', views.bedrift, name='bedrift'),
    url(r'^(?P<pk>[0-9]+)/kommenter/$', views.comment, name='comment'),
    url(r'^bedrift/bedpress/(?P<pk>[0-9]+)$', views.bedpress, name='bedpress'),
    url(r'^(?P<pk>[0-9]+)/comment$', comment_company, name='comment_company'),
    url(r'^/bedpress/(?P<pk>[0-9]+)/comment$', bedpress_company_comment, name='bedpress_company_comment'),

]
