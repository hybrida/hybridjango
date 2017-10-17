from django.conf.urls import url

from .views import *


urlpatterns = [
                  url(r'^$', BadgeView.as_view(template_name='achievments/achievments_overview.html') ,name='achievements'),
]