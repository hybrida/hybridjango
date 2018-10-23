from django.conf.urls import url
from .views import BadgeTable, DeleteBadge

from .views import *


urlpatterns = [
        url(r'^badges/$', BadgeView.as_view(template_name='achievements/achievments_overview.html'), name='achievements'),
        url(r'^current/$', ScoreboardViewCurrent.as_view(template_name='achievements/scoreboard.html'), name='scoreboard'),
        url(r'^all_time/$', ScoreboardViewAllTime.as_view(template_name='achievements/scoreboard.html'), name='scoreboard/AllTime'),
        url(r'^badgeform/add/$', SendBadge.as_view(), name='badgeform-add'),
        url(r'^badgeform/table/$', BadgeTable, name='badgetable'),
        url(r'^badgeform/(?P<pk>[0-9]+)/delete', DeleteBadge.as_view(), name='badgeform-delete'),
        url(r'^badgeRequest/add/', add_badge_request, name='badgerequest-add'),
        url(r'^badgeRequest/table/', badge_request_table, name='badgerequest-table'),
        url(r'^badgerequest/(?P<pk>[0-9]+)/delete', BadgeRequestDelete.as_view(), name='badgerequest-delete'),
]
