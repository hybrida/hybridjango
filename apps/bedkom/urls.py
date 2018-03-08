from django.conf.urls import url
from .views import *
from apps.bedkom.views import comment_company, bedpress_company_comment

urlpatterns = [
    url(r'^$', index, name='bedkom'),
    url(r'^bedrift/(?P<pk>[0-9]+)$', bedrift, name='bedrift'),
    url(r'^(?P<pk>[0-9]+)/kommenter/$', comment, name='comment'),
    url(r'^bedrift/bedpress/(?P<pk>[0-9]+)$', bedpress, name='bedpress'),
    url(r'^(?P<pk>[0-9]+)/comment$', comment_company, name='comment_company'),
    url(r'^bedpress/(?P<pk>[0-9]+)/comment$', bedpress_company_comment, name='bedpress_company_comment'),
    url(r'^bedrift/ny', new_company, name='new_company'),
    url(r'^bedrift/(?P<pk>[0-9]+)/endre$', edit_company, name='edit_company'),
    url(r'^(?P<pk>[0-9]+)/comment2$', comment_company2, name='comment_company2'),
    url(r'^(?P<pk>[0-9]+)/endre/statusprority', edit_status_priority_comment, name='edit_status_priority_comment')
]
