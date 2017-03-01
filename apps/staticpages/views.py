import os
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import resolve
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from apps.registration.models import get_graduation_year
from apps.events.models import Event
from apps.events.views import EventList
from apps.jobannouncements.models import Job
from apps.registration.models import Hybrid
from hybridjango.settings import STATIC_FOLDER


class FrontPage(EventList):
    model = EventList.model
    queryset = EventList.queryset

    def get_context_data(self, **kwargs):

        tz = timezone.get_current_timezone()
        temporary_quickfix_for_tp_events = [
            Event(pk=-1, title='Bedriftspresentasjon med DNV GL', event_start=tz.localize(datetime(2017, 1, 25, 17, 30, 0)), text='431'),
            Event(pk=-1, title='Karrieremesse med Framtidsfylket', event_start=tz.localize(datetime(2017, 1, 26, 17)), text='407'),
            Event(pk=-1, title='Prospective', event_start=tz.localize(datetime(2017, 2, 9)), text='440'),
            Event(pk=-1, title='DNB Digital Challenge', event_start=tz.localize(datetime(2017, 2, 10)), text='430'),
            Event(pk=-1, title='Karrieremesse med Haugesundsregionen', event_start=tz.localize(datetime(2017, 2, 16, 18)), text='406'),
            Event(pk=-1, title='DNV GL Opportunity Day', event_start=tz.localize(datetime(2017, 3, 2, 10, 15)), text='432'),
            Event(pk=-1, title='Teknologiporten FOKUS: InnoVention', event_start=tz.localize(datetime(2017, 3, 16, 17)), text='422'),
            Event(pk=-1, title='AF Gruppen', event_start=tz.localize(datetime(2017, 2, 1, 17, 15)), text='428'),
            Event(pk=-1, title='Multiconsult', event_start=tz.localize(datetime(2017, 2, 8, 17)), text='391'),
        ]

        context = super(EventList, self).get_context_data(**kwargs)
        event_list_chronological = Event.objects.filter(
            event_start__gte=timezone.now(), bedpress__isnull=True
        )
        bedpress_list_chronological = Event.objects.filter(event_start__gte=timezone.now(), bedpress__isnull=False, hidden=False)
        if not self.request.user.is_authenticated:
            event_list_chronological = event_list_chronological.filter(public=True)
            bedpress_list_chronological = bedpress_list_chronological.filter(public=True)

        context['event_list_chronological'] = event_list_chronological.order_by('event_start')[:7]
        context['bedpress_list_chronological'] = sorted(chain(bedpress_list_chronological.order_by('event_start')[:7],
                     [tp_event for tp_event in temporary_quickfix_for_tp_events if tp_event.event_start > timezone.now()]
                     ), key=lambda event: event.event_start)[:7]

        context['job_list'] = Job.objects.filter(deadline__gte=timezone.now()).order_by('-weight','deadline').filter(priority=True)
        context['job_sidebar'] = Job.objects.filter(deadline__gte=timezone.now())
        return context


aboutpages = [
    ('about', "Om Hybrida"),
    ('history', "Hybridas historie"),
    ('board', "Styret"),
    ('committees', "Komiteer"),
    ('griff_orden', "Griffens Orden"),
    ('statutter', "Statutter"),
    ('tillitsvalgte','Tillitsvalgte'),
    ('studiet', "Studiet I&IKT"),
    ('holte', "Holte Consulting"),
    ('lyrics', "Sangtekster"),
    ('for_companies', "For bedrifter"),
    ('contact_us', "Kontakt oss"),
]


class AboutView(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
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
            'leder': Hybrid.objects.get(username='martiaks'),
            'nestleder': Hybrid.objects.get(username='sigribra'),
            'skattmester': Hybrid.objects.get(username='shahiths'),
            'bksjef': Hybrid.objects.get(username='ludviglj'),
            'festivalus': Hybrid.objects.get(username='njknudse'),
            'vevsjef': Hybrid.objects.get(username='anstra'),
            'jentekomsjef': Hybrid.objects.get(username='andrsly'),
            'redaktor': Hybrid.objects.get(username='amaliams'),
        }) # Can be initialized only on startup (using middleware for example) if it becomes too costly
        return self.render_to_response(context)


ringenpages = [
    ('ringen', "Ringen"),
    ('ringen_IIKT', 'Studiet I&IKT'),
    ('ringen_visjon', 'Visjon'),
    ('ringen_styret', 'Styret'),
    ('ringen_bidrag', 'Bedriftens Bidrag'),
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
    context = {
        'object_list': Event.objects.filter(title__icontains=query),
    }
    return render(request, 'staticpages/search.html', context)
