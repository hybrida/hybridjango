import os
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import resolve
from django.utils import timezone
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View

from apps.events.models import Event, TPEvent
from apps.events.views import EventList
from apps.jobannouncements.models import Job
from apps.registration.models import Hybrid
from apps.registration.models import get_graduation_year
from apps.staticpages.models import BoardReport, Protocol
from hybridjango.settings import STATIC_FOLDER


class FrontPage(EventList):
    model = EventList.model
    queryset = EventList.queryset

    def get_context_data(self, **kwargs):
        tp_events = TPEvent.objects.filter(event_start__gte=timezone.now())

        context = super(EventList, self).get_context_data(**kwargs)
        event_list_chronological = Event.objects.filter(
            event_start__gte=timezone.now(), bedpress__isnull=True, hidden=False
        )
        bedpress_list_chronological = Event.objects.filter(event_start__gte=timezone.now(), bedpress__isnull=False,
                                                           hidden=False)
        if not self.request.user.is_authenticated:
            event_list_chronological = event_list_chronological.filter(public=True)
            bedpress_list_chronological = bedpress_list_chronological.filter(public=True)

        context['event_list_chronological'] = event_list_chronological.order_by('event_start')[:7]
        context['bedpress_list_chronological'] = sorted(chain(bedpress_list_chronological.order_by('event_start')[:7],
                                                              [tp_event for tp_event in tp_events
                                                               if tp_event.event_start > timezone.now()]
                                                              ), key=lambda event: event.event_start)[:7]

        context['job_list'] = Job.objects.filter(deadline__gte=timezone.now()).order_by('-weight', 'deadline').filter(
            priority=True)
        context['job_sidebar'] = Job.objects.filter(deadline__gte=timezone.now())
        return context


aboutpages = [
    ('about', "Om Hybrida"),
    ('history', "Hybridas historie"),
    ('board', "Styret"),
    ('committees', "Komiteer"),
    ('griffensorden', "Griffens Orden"),
    ('statutter', "Statutter"),
    ('tillitsvalgte', 'Tillitsvalgte'),
    ('studiet', "Studiet I&IKT"),
    ('holte', "Holte Consulting"),
    ('lyrics', "Sangtekster"),
    ('for_companies', "For bedrifter"),
    ('contact_us', "Kontakt oss"),
]


class AboutView(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'active_page' in context.keys():
            active_page = context['active_page']
        else:
            active_page = resolve(request.path_info).url_name
        before_pages = []
        after_pages = []
        page_found = False
        for page in aboutpages:
            if page_found:
                after_pages.append(page)
            else:
                before_pages.append(page)
                if page[0] == active_page:
                    page_found = True

        context['before_pages'] = before_pages
        context['after_pages'] = after_pages
        context.update({
            'leder': Hybrid.objects.get(username='ludviglj'),
            'nestleder': Hybrid.objects.get(username='torasg'),
            'skattmester': Hybrid.objects.get(username='torstsol'),
            'bksjef': Hybrid.objects.get(username='jonasvja'),
            'festivalus': Hybrid.objects.get(username='rikkebl'),
            'vevsjef': Hybrid.objects.get(username='sindreeo'),
            'jentekomsjef': Hybrid.objects.get(username='renatebf'),
            'redaktor': Hybrid.objects.get(username='kriraae'),
        })  # Can be initialized only on startup (using middleware for example) if it becomes too costly
        return self.render_to_response(context)


ringenpages = [
    ('ringen', "Ringen"),
    ('ringen_IIKT', 'Studiet I&IKT'),
    ('ringen_visjon', 'Visjon'),
    ('ringen_styret', 'Styret'),
    ('ringen_medlemmer', 'Medlemmer'),
    ('ringen_promotering', 'Promotering'),
    ('ringen_kontakt', 'Kontaktinformasjon'),
]


def members(request):
    if request.method == 'GET':
        endyear = get_graduation_year(1)
    elif request.method == 'POST':
        endyear = get_graduation_year(request.POST.get("grade"))
    return render(request, "staticpages/students.html",
                  {'students': Hybrid.objects.filter(graduation_year=endyear).order_by('last_name')})


class ProtocolView(LoginRequiredMixin, AboutView):
    def get_context_data(self, **kwargs):
        context = super(ProtocolView, self).get_context_data(**kwargs)
        context['protocols'] = Protocol.objects.all().order_by('date').reverse()
        context['active_page'] = 'statutter'
        return context

class BoardReportView(LoginRequiredMixin, AboutView):
    def get_context_data(self, **kwargs):
        context = super(BoardReportView, self).get_context_data(**kwargs)
        context['reports'] = BoardReport.objects.all().order_by('date').reverse()
        context['active_page'] = 'board'
        return context


class RingenView(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        active_page = resolve(request.path_info).url_name
        before_pages = []
        after_pages = []
        page_found = False
        for page in ringenpages:
            if page_found:
                after_pages.append(page)
            else:
                before_pages.append(page)
                if page[0] == active_page:
                    page_found = True

        context['before_pages'] = before_pages
        context['after_pages'] = after_pages
        context['ringen'] = 'img/bannerIKT.png'
        return self.render_to_response(context)


UPDATEK = os.path.join(STATIC_FOLDER, 'pdf/updatek')


def updatek(request):
    context = {}
    dirs = os.listdir(UPDATEK)
    context['updatek'] = sorted([(
                                     dir,
                                     sorted(set([os.path.splitext(file)[0] for file in
                                                 os.listdir(os.path.join(UPDATEK, dir))]))
                                 ) for dir in dirs], key=lambda dir: dir[0], reverse=True)
    return render(request, 'staticpages/updatek.html', context)


@login_required
def search(request):
    query = request.GET['tekst']
    from itertools import chain
    event_object = Event.objects.filter(title__icontains=query)
    job_object_title = Job.objects.filter(title__icontains=query)
    job_object_company = Job.objects.filter(company__name__icontains=query)
    user_object_username = Hybrid.objects.filter(username__icontains=query)

    complete_list = list(chain(event_object, job_object_title, job_object_company, user_object_username,))
    print(complete_list)

    context = {
        'object_list': complete_list,

    }
    return render(request, 'staticpages/search.html', context)
