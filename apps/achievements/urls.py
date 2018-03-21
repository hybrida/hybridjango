from django.conf.urls import url
from .views import BadgeTable, DeleteBadge

from .views import *


urlpatterns = [
        url(r'^badges/$', BadgeView.as_view(template_name='achievements/achievments_overview.html'), name='achievements'),
        url(r'^current/$', ScoreboardViewCurrent.as_view(template_name='achievements/scoreboard.html'), name='scoreboard'),
        url(r'^all_time/$', ScoreboardViewAllTime.as_view(template_name='achievements/scoreboard.html'), name='scoreboard/AllTime'),
        url(r'^badgeform/add/$', SendBadge.as_view(), name='badgeform-add'),
        url(r'^badgeform/table/$', BadgeTable, name='badgetable'),

]
