import json
from os import path
from .models import BadgeSuggestion
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from .forms import BadgeRequestForm, BadgeForm, BadgeSuggestionForm
from .models import Badge, BadgeRequest
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404


class CreateSuggestion(CreateView):
    form_class = BadgeSuggestionForm
    template_name = 'achievements/badgesuggestion_form.html'
    success_url = reverse_lazy('scoreboard')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.suggested_by = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)

class DeleteBadge(DeleteView):
    model = BadgeSuggestion
    success_url = reverse_lazy('badgesuggestion-table')


def badge_suggestions_table(request):
    if request.method == 'POST':
        suggestion = BadgeSuggestion.objects.get(pk=int(request.POST.get("suggestion-id")))

        # Use image from suggestion or the one uploaded in form
        if request.POST.get('use-suggested-image') == 'on':
            image = suggestion.image
        else:
            image = request.FILES.get('badge_image')

        # use django form validation
        form = BadgeForm(request.POST, {'badge_image': image})
        if form.is_valid():
            form.save()

            # give contributor badge to whoever gave the suggestion
            if request.POST.get('give-contrib-badge') == 'on' and suggestion.suggested_by:
                Badge.objects.get(name="Contributor").user.add(suggestion.suggested_by)

            # don't need the suggestion after the badge is created
            suggestion.delete()

        return HttpResponseRedirect('#')

    # suggestions as dict rather than list for js indexing by id
    suggestions = {
        suggestion.id: {
            'name': suggestion.name,
            'description': suggestion.description,
            'award_to': suggestion.award_to,
            'image_url': suggestion.image.url,
            'scorepoints': suggestion.scorepoints,
            # js doesn't like Hybrid objects or None, so we replace them with strings
            'suggested_by': suggestion.suggested_by.full_name if suggestion.suggested_by else ""
        } for suggestion in BadgeSuggestion.objects.all()
    }
    return render(request, '../templates/achievements/badgesuggestion_table.html', {
        "suggestions": suggestions,
        "form": BadgeForm()
    })


def overview(request):
    return render(request, '../templates/achievements/achievments_overview.html')


def badge_request_data(request, badge_id):
    print('and I aint never stopped')
    badge = get_object_or_404(Badge, pk=badge_id)
    data = {
        "name": badge.name,
        "description": badge.description,
        "scorepoints": badge.scorepoints,
        "badge_image": str(badge.badge_image),
        "user_has": badge in request.user.hybridbadges.all()
    }
    queryset = BadgeRequest.objects.filter(badge=badge, user=request.user)
    if queryset.exists():
        req = queryset.first()
        data["request"] = {
            "status": req.get_status_display(),
            "comment": req.comment
        }
    return JsonResponse(data)


class BadgeView(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #Adding the badges to the context to find them in the html file
        context.update({
            'Badges': Badge.objects.all()
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
