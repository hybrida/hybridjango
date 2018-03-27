import json
from os import path
from .models import BadgeForm
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.views.generic.edit import CreateView, DeleteView

from .models import Badge


class SendBadge(CreateView):
    model = BadgeForm
    fields = ['name', 'description', 'badge_image', 'scorepoints']


class DeleteBadge(DeleteView):
    model = BadgeForm
    success_url = reverse_lazy('scoreboard')


def BadgeTable(request):
    badge_forms = BadgeForm.objects.all()
    return render(request, '../templates/achievements/badeform_table.html', {"badge_forms": badge_forms})


def overview(request):
    return render(request, '../templates/achievements/achievments_overview.html', )


class BadgeView(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #Adding the badges to the context to find them in the html file
        context.update({
            'Badges': Badge.objects.all(),
        })

        return self.render_to_response(context)


class ScoreboardViewCurrent(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        current = True #Used in the html file to know that it's the current scoreboard

        #Reading the current scoreboard .json file in /uploads
        with open(path.join(settings.MEDIA_ROOT, 'ScoreboardCurrent.json'), encoding='utf-8') as data_file:
            scorelist = json.loads(data_file.read())
        #Adding the badges, current status and the scoreboard to the context to find them in the html file
        context.update({
            'Badges': Badge.objects.all(),
            'Scorelist': scorelist,
            'Current': current,
        })

        return self.render_to_response(context)

class ScoreboardViewAllTime(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        current = False#Used in the html file to know that it's the all time scoreboard

        # Reading the all time scoreboard .json file in /uploads
        with open(path.join(settings.MEDIA_ROOT, 'ScoreboardAllTime.json'), encoding='utf-8') as data_file:
            scorelist = json.loads(data_file.read())
        # Adding the badges, current status and the scoreboard to the context to find them in the html file
        context.update({
            'Badges': Badge.objects.all(),
            'Scorelist': scorelist,
            'Current': current,
        })

        return self.render_to_response(context)
