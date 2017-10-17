from django.shortcuts import render
from .models import Badge
from django.urls import resolve
from apps.registration.models import Hybrid
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View



def overview(request):
    return render(request, '../templates/achievments/achievments_overview.html',)

class  BadgeView (TemplateResponseMixin, ContextMixin, View):
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

        # this needs to be fixed/improved upon

        context['before_pages'] = before_pages
        context['after_pages'] = after_pages

        context.update({
            'Badges': Badge.objects.all(),
        })

        return self.render_to_response(context)

aboutpages = [
    ('about', "Om Hybrida"),
    ('history', "Hybridas historie"),
    ('board', "Styret"),
    ('committees', "Komiteer"),
    ('griffensorden', "Griffens Orden"),
    ('statutter', "Statutter"),
    ('tillitsvalgte','Tillitsvalgte'),
    ('studiet', "Studiet I&IKT"),
    ('holte', "Holte Consulting"),
    ('lyrics', "Sangtekster"),
    ('for_companies', "For bedrifter"),
    ('contact_us', "Kontakt oss"),
]