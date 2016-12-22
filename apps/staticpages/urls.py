from django.conf.urls import url
from django.views.generic import TemplateView

from apps.events.views import updatek

urlpatterns = [
    url(r'^strikk/', TemplateView.as_view(template_name='staticpages/hybridastrikk.html')),
    url(r'^statutter/', TemplateView.as_view(template_name='staticpages/statutter.html'), name='statutter'),
    url(r'^griffens_orden/', TemplateView.as_view(template_name='staticpages/griffens_orden.html'), name='griff_orden'),
    url(r'^om_hybrida/', TemplateView.as_view(template_name='staticpages/about.html'), name='about'),
    url(r'^for_bedrifter/', TemplateView.as_view(template_name='staticpages/for_companies.html'),
        name='for_companies'),
    url(r'^updatek/', updatek, name='updatek'),
    url(r'^komite/', TemplateView.as_view(template_name='staticpages/committees.html'), name='committees'),
    url(r'^kontakt_oss/', TemplateView.as_view(template_name='staticpages/contact_us.html'), name='contact_us'),
    url(r'^sangtekster/', TemplateView.as_view(template_name='staticpages/lyrics.html'), name='lyrics'),
]
