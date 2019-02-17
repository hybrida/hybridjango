import json
from os import path
from .models import BadgeForslag
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from .forms import BadgeRequestForm
from .models import Badge, BadgeRequest
from django.http import HttpResponseRedirect, HttpResponseNotFound


class SendBadge(CreateView):
    model = BadgeForslag
    fields = ['navn', 'beskrivelse', 'tildeles', 'badge_bilde', 'scorepoints']


class DeleteBadge(DeleteView):
    model = BadgeForslag
    success_url = reverse_lazy('badgetable')


def BadgeTable(request):
    badge_forms = BadgeForslag.objects.all()
    return render(request, '../templates/achievements/badeform_table.html', {"badge_forms": badge_forms})


def overview(request):
    return render(request, '../templates/achievements/achievments_overview.html')


class BadgeView(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        data = {}
        user_badges = request.user.hybridbadges.all()
        for badge in Badge.objects.all():
            data[badge.id] = {
                "name": badge.name,
                "description": badge.description,
                "scorepoints": badge.scorepoints,
                "badge_image": str(badge.badge_image),
                "user_has": badge in user_badges
            }
            queryset = BadgeRequest.objects.filter(badge=badge, user=request.user)
            if queryset.exists():
                req = queryset.first()
                data[badge.id]["request"] = {
                    "status": req.get_status_display(),
                    "comment": req.comment
                }
        context = self.get_context_data(**kwargs)
        #Adding the badges to the context to find them in the html file
        context.update({
            'Badges': Badge.objects.all(),
            'data': json.dumps(data),
            'form': BadgeRequestForm()
        })

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        BadgeRequest.objects.create(
            user=request.user,
            badge=Badge.objects.get(id=request.POST.get("badge-id", -1)),
            comment=request.POST.get("comment", ""),
            status=BadgeRequest.PENDING
        )
        return HttpResponseRedirect('#')


class BadgeRequestView(PermissionRequiredMixin, TemplateResponseMixin, ContextMixin, View):
    permission_required = 'achievements.can_change_badgerequest'

    def get(self, request, status, **kwargs):
        if status == "all":
            requests = BadgeRequest.objects.all()
        elif status == "approved":
            requests = BadgeRequest.objects.filter(status=BadgeRequest.APPROVED)
        elif status == "denied":
            requests = BadgeRequest.objects.filter(status=BadgeRequest.DENIED)
        elif status == "pending" or status == "":
            requests = BadgeRequest.objects.filter(status=BadgeRequest.PENDING)
        else:
            return HttpResponseNotFound("Not a valid argument; try approved, denied, pending or nothing")
        context = self.get_context_data(**kwargs)
        context.update({
            'requests': requests,
            'status': status
        })
        return self.render_to_response(context)

    def post(self, request, status, **kwargs):
        if "approve" in request.POST:
            BadgeRequest.objects.get(id=request.POST.get("request-id", -1)).approve()
        elif "deny" in request.POST:
            BadgeRequest.objects.get(id=request.POST.get("request-id", -1)).deny()
        elif "pending" in request.POST:
            BadgeRequest.objects.get(id=request.POST.get("request-id", -1)).set_pending()
        return HttpResponseRedirect('#')


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
