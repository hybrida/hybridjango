from django.conf.urls import url
from .views import *

urlpatterns = [
            url(r'^$', GriffenView.as_view(template_name='griffensorden/griffens_orden.html'), name='griffensorden'),
        ]