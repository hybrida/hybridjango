from django.shortcuts import render
from django.urls import resolve
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from apps.achievements.signals.signals import *
from apps.achievements.forms import *
from .models import Badge
from apps.registration.models import Hybrid
from datetime import datetime



def overview(request):
    return render(request, '../templates/achievments/achievments_overview.html', )


class BadgeView(TemplateResponseMixin, ContextMixin, View):
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


class ScoreboardViewCurrent(TemplateResponseMixin, ContextMixin, View):
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

        # lager en liste med hybrider og scorepoints
        scorelist = []

        for hybrid in Hybrid.objects.all():

            grad_year = hybrid.graduation_year
            current_year = int(datetime.now().year)  # Getting the current datetime

            if grad_year - current_year >= 0:

                score = 0

                username = hybrid.username
                full_name = hybrid.full_name

                for badge in Badge.objects.all():
                    for user in badge.user.all():
                        if username in user.username:

                            score += badge.scorepoints

                hybrid_dict= {
                    'Name': username,
                    'Score': score,
                    'Full_Name': full_name,
                    'Number': 0,
                }

                scorelist.append(hybrid_dict)

        switch = True

        while(switch):

            switch = False
            for i in range(len(scorelist) - 1 ):

                hybrid1 = scorelist[i]
                hybrid2 = scorelist[i+1]

                if hybrid1['Score'] < hybrid2['Score']:

                    scorelist[i] = hybrid2
                    scorelist[i+1] = hybrid1

                    switch = True

        x = 0

        for item in scorelist:
            x += 1
            item['Number'] = x


        context['before_pages'] = before_pages
        context['after_pages'] = after_pages

        context.update({
            'Badges': Badge.objects.all(),
            'Scorelist': scorelist,
        })

        return self.render_to_response(context)

class ScoreboardViewAllTime(TemplateResponseMixin, ContextMixin, View):
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

        # lager en liste med hybrider og scorepoints
        scorelist = []
        x = 0
        for hybrid in Hybrid.objects.all():
            score = 0
            x += 1
            name = hybrid.username
            full_name = hybrid.full_name
            for badge in Badge.objects.all():
                for user in badge.user.all():
                    if name in user.username:
                        score += badge.scorepoints
            dict = {
                'Name': name,
                'Score': score,
                'Full_Name': full_name,
                'X':x,
            }
            scorelist.append(dict)

        switch = True

        while (switch):

            switch = False
            for i in range(len(scorelist) - 1):

                hybrid1 = scorelist[i]
                hybrid2 = scorelist[i + 1]

                if hybrid1['Score'] < hybrid2['Score']:
                    scorelist[i] = hybrid2
                    scorelist[i + 1] = hybrid1

                    switch = True

        x = 0

        for item in scorelist:
            x += 1
            item['Number'] = x


        context['before_pages'] = before_pages
        context['after_pages'] = after_pages

        context.update({
            'Badges': Badge.objects.all(),
            'Scorelist': scorelist,
        })

        return self.render_to_response(context)


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
