from django.conf.urls import url
from django.views.generic import TemplateView

from apps.staticpages.views import AboutView, updatek, search

urlpatterns = [
    url(r'^s[oø]k/', search, name='search'),
    url(r'^strikk/', TemplateView.as_view(template_name='staticpages/hybridastrikk.html')),
    url(r'^statutter/', AboutView.as_view(template_name='staticpages/statutter.html'), name='statutter'),
    url(r'^griffens_orden/', AboutView.as_view(template_name='staticpages/griffens_orden.html'), name='griff_orden'),
    url(r'^om_hybrida/', AboutView.as_view(template_name='staticpages/about.html'), name='about'),
    url(r'^for_bedrifter/', AboutView.as_view(template_name='staticpages/for_companies.html'), name='for_companies'),
    url(r'^updatek/', updatek, name='updatek'),
    url(r'^komite/', AboutView.as_view(template_name='staticpages/committees.html'), name='committees'),
    url(r'^styret/', AboutView.as_view(template_name='staticpages/board.html'), name='board'),
    url(r'^kontakt_oss/', AboutView.as_view(template_name='staticpages/contact_us.html'), name='contact_us'),
    url(r'^sangtekster/', AboutView.as_view(template_name='staticpages/lyrics.html'), name='lyrics'),
]
