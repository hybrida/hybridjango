import os

from django.shortcuts import render
from django.urls import resolve
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from apps.jobannouncements.models import Job
from django.utils import timezone

from apps.events.views import EventList
from apps.registration.models import Hybrid
from hybridjango.settings import STATIC_FOLDER


class FrontPage(EventList):
    model = EventList.model
    queryset = EventList.queryset

    def get_context_data(self, **kwargs):
        context_data = EventList.get_context_data(self, **kwargs)
        context_data['jobs'] = Job.objects.filter(deadline__gte=timezone.now()).order_by('-timestamp')
        return context_data

aboutpages = [
    ('about', "Om Hybrida"),
    ('contact_us', "Kontakt Oss"),
    ('board', "Styret"),
    ('committees', "Komiteer"),
    ('griff_orden', "Griffens Orden"),
    ('statutter', "Statutter"),
    ('lyrics', "Sangtekster"),
    ('for_companies', "For Bedrifter"),
]

contact_people = {
        'leder': Hybrid.objects.get(username='martiaks'),
        'nestleder': Hybrid.objects.get(username='sigribra'),
        'skattmester': Hybrid.objects.get(username='jonasasa'),
        'bksjef': Hybrid.objects.get(username='ludviglj'),
        'festivalus': Hybrid.objects.get(username='njknudse'),
        'vevsjef': Hybrid.objects.get(username='simennje'),
        'jentekomsjef': Hybrid.objects.get(username='gurogb'),
        'redaktor': Hybrid.objects.get(username='hanneove'),
}

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
        context.update(contact_people)
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