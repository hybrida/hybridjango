from django.conf.urls import url

from .views import *


urlpatterns = [
        url(r'^badges/$', BadgeView.as_view(template_name='achievments/achievments_overview.html'), name='achievements'),
        url(r'^current/$', ScoreboardViewCurrent.as_view(template_name='achievments/scoreboard.html'), name='scoreboard'),
        url(r'^all_time/$', ScoreboardViewAllTime.as_view(template_name='achievments/scoreboard.html'), name='scoreboard/AllTime'),

]