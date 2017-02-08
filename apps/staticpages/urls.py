from django.conf.urls import url
from django.views.generic import TemplateView

from apps.staticpages.views import AboutView, updatek, search, RingenView

urlpatterns = [
    url(r'^s[oø]k/$', search, name='search'),
    url(r'^strikk/$', TemplateView.as_view(template_name='staticpages/hybridastrikk.html')),
    url(r'^statutter/$', AboutView.as_view(template_name='staticpages/statutter.html'), name='statutter'),
    url(r'^griffens_orden/$', AboutView.as_view(template_name='staticpages/griffens_orden.html'), name='griff_orden'),
    url(r'^om_hybrida/$', AboutView.as_view(template_name='staticpages/about.html'), name='about'),
    url(r'^for_bedrifter/$', AboutView.as_view(template_name='staticpages/for_companies.html'), name='for_companies'),
    url(r'^updatek/$', updatek, name='updatek'),
    url(r'^komite/$', AboutView.as_view(template_name='staticpages/committees.html'), name='committees'),
    url(r'^styret/$', AboutView.as_view(template_name='staticpages/board.html'), name='board'),
    url(r'^kontakt_oss/$', AboutView.as_view(template_name='staticpages/contact_us.html'), name='contact_us'),
    url(r'^sangtekster/$', AboutView.as_view(template_name='staticpages/lyrics.html'), name='lyrics'),
    url(r'^historie/$', AboutView.as_view(template_name='staticpages/history.html'), name='history'),
    url(r'^tillitsvalgte/$',AboutView.as_view(template_name='staticpages/tillitsvalgte.html'), name='tillitsvalgte'),
    #url(r'^holte/$', AboutView.as_view(template_name='staticpages/holte.html'), name='holte'),
    url(r'^studiet', AboutView.as_view(template_name='staticpages/ringen/studiet.html'), name='studiet'),
    url(r'^ringen/$', RingenView.as_view(template_name='staticpages/ringen.html'), name='ringen'),
    url(r'^ringen/studiet', RingenView.as_view(template_name='staticpages/ringen/studiet.html'), name='ringen_IIKT'),
    url(r'^ringen/visjon', RingenView.as_view(template_name='staticpages/ringen/visjon.html'), name='ringen_visjon'),
    url(r'^ringen/styret', RingenView.as_view(template_name='staticpages/ringen/styret.html'), name='ringen_styret'),
    url(r'^ringen/medlemmer', RingenView.as_view(template_name='staticpages/ringen/medlemmer.html'), name='ringen_medlemmer'),
    url(r'^ringen/bedriftens_bidrag', RingenView.as_view(template_name='staticpages/ringen/bidrag.html'), name='ringen_bidrag'),
    url(r'^ringen/promotering', RingenView.as_view(template_name='staticpages/ringen/promotering.html'), name='ringen_promotering'),
    url(r'^ringen/kontakt', RingenView.as_view(template_name='staticpages/ringen/kontakt.html'), name='ringen_kontakt'),
]
