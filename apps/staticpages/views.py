import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import resolve
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.utils import timezone

from hybridjango.settings import STATIC_FOLDER

from apps.events.models import Event
from apps.events.views import EventList
from apps.registration.models import Hybrid
from apps.jobannouncements.models import Job


class FrontPage(EventList):
    model = EventList.model
    queryset = EventList.queryset

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context['event_list_chronological'] = Event.objects.filter(
            event_start__gte=timezone.now(), bedpress__isnull=True
        ).order_by('event_start')[:5]
        context['bedpress_list_chronological'] = Event.objects.filter(
            event_start__gte=timezone.now(), bedpress__isnull=False
        ).order_by('event_start')[:5]
        context['jobs'] = Job.objects.filter(deadline__gte=timezone.now()).order_by('-deadline')
        return context


aboutpages = [
    ('about', "Om Hybrida"),
    ('contact_us', "Kontakt oss"),
    ('board', "Styret"),
    ('committees', "Komiteer"),
    ('griff_orden', "Griffens Orden"),
    ('statutter', "Statutter"),
    ('lyrics', "Sangtekster"),
    ('for_companies', "For bedrifter"),
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
            'skattmester': Hybrid.objects.get(username='jonasasa'),
            'bksjef': Hybrid.objects.get(username='ludviglj'),
            'festivalus': Hybrid.objects.get(username='njknudse'),
            'vevsjef': Hybrid.objects.get(username='simennje'),
            'jentekomsjef': Hybrid.objects.get(username='gurogb'),
            'redaktor': Hybrid.objects.get(username='hanneove'),
        }) # Can be initialized only on startup (using middleware for example) if it becomes too costly
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
