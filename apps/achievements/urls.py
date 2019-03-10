from django.conf.urls import url

from .views import *


urlpatterns = [
        url(r'^badges/$', BadgeView.as_view(template_name='achievements/achievments_overview.html'), name='achievements'),
        url(r'^current/$', ScoreboardViewCurrent.as_view(template_name='achievements/scoreboard.html'), name='scoreboard'),
        url(r'^all_time/$', ScoreboardViewAllTime.as_view(template_name='achievements/scoreboard.html'), name='scoreboard/AllTime'),
        url(r'^suggestion/add/$', CreateSuggestion.as_view(), name='badgesuggestion-add'),
        url(r'^suggestion/table/$', badge_suggestions_table, name='badgesuggestion-table'),
        url(r'^suggestion/(?P<pk>[0-9]+)/delete', DeleteBadge.as_view(), name='badgesuggestion-delete'),
        url(r'^badges/requests/(?P<status>.*)$', BadgeRequestView.as_view(template_name='achievements/badgerequest_table.html'), name='badgerequest-list')
]
