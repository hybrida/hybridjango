from django.conf.urls import url
from django.views.generic import TemplateView

from apps.staticpages.views import AboutView, updatek, search, RingenView, members, BoardReportView, ProtocolView, \
    application, application_table, DeleteApplication, AddComApplication, commiteapplications, NewStudent, edit_application, ChangeAcceptedStatus, KTVReportView

urlpatterns = [
    url(r'^s[oø]k$', search, name='search'),
    url(r'^nystudent$', NewStudent, name='newstudent'),
    url(r'^strikk$', TemplateView.as_view(template_name='staticpages/hybridastrikk.html'), name="strikk"),
    url(r'^statutter$', AboutView.as_view(template_name='staticpages/statutter.html'), name='statutter'),
    url(r'^statutter/protokoller/$', ProtocolView.as_view(template_name='staticpages/protocols.html'),
        name='protocols'),
    url(r'^om_hybrida$', AboutView.as_view(template_name='staticpages/about.html'), name='about'),
    url(r'^for_bedrifter$', AboutView.as_view(template_name='staticpages/for_companies.html'), name='for_companies'),
    url(r'^updatek$', updatek, name='updatek'),
    url(r'^komite$', AboutView.as_view(template_name='staticpages/committees.html'), name='committees'),
    url(r'^interessegrupper$', AboutView.as_view(template_name='staticpages/interest_groups.html'), name='interest_groups'),
    url(r'^styret$', AboutView.as_view(template_name='staticpages/board.html'), name='board'),
    url(r'^styret/referat$', BoardReportView.as_view(template_name='staticpages/board_report.html'),
        name='board_report'),
    url(r'^kontakt_oss$', AboutView.as_view(template_name='staticpages/contact_us.html'), name='contact_us'),
    url(r'^sangtekster$', AboutView.as_view(template_name='staticpages/lyrics.html'), name='lyrics'),
    url(r'^historie$', AboutView.as_view(template_name='staticpages/history.html'), name='history'),
    url(r'^tillitsvalgte$', AboutView.as_view(template_name='staticpages/tillitsvalgte.html'), name='tillitsvalgte'),
    url(r'^holte$', AboutView.as_view(template_name='staticpages/holte.html'), name='holte'),
    url(r'^studiet$', AboutView.as_view(template_name='staticpages/ringen/studiet.html'), name='studiet'),
    url(r'^soknad/form$', application, name='application-add'),
    url(r'^soknad/table$', application_table, name='application_table'),
    url(r'^application/(?P<pk>[0-9]+)/delete$', DeleteApplication.as_view(), name='application-delete'),
    url(r'^ringen$', RingenView.as_view(template_name='staticpages/ringen.html'), name='ringen'),
    url(r'^ringen/studiet$', RingenView.as_view(template_name='staticpages/ringen/studiet.html'), name='ringen_IIKT'),
    url(r'^ringen/visjon$', RingenView.as_view(template_name='staticpages/ringen/visjon.html'), name='ringen_visjon'),
    url(r'^ringen/styret$', RingenView.as_view(template_name='staticpages/ringen/styret.html'), name='ringen_styret'),
    url(r'^ringen/medlemmer$', RingenView.as_view(template_name='staticpages/ringen/medlemmer.html'),
        name='ringen_medlemmer'),
    url(r'^ringen/promotering$', RingenView.as_view(template_name='staticpages/ringen/promotering.html'),
        name='ringen_promotering'),
    url(r'^ringen/kontakt$', RingenView.as_view(template_name='staticpages/ringen/kontakt.html'),
        name='ringen_kontakt'),
    url(r'^studenter$', members, name='members'),
    url(r'^sokkomite', AddComApplication, name='comApp-add'),
    url(r'^komiteersok', commiteapplications, name='comapps'),
    url(r'(?P<pk>[0-9]+)/applications/edit', edit_application, name='edit_application'),
    url(r'^change_accepted_status', ChangeAcceptedStatus, name='change_accepted_status'),
    url(r'itvreferat', KTVReportView.as_view(template_name="staticpages/ITVprotocols.html"), name="KTVreport")
]
