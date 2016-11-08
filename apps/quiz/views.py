from django.http import HttpResponse
from django.template import loader
from .models import Team


def index(request):
    best_team = Team.objects.order_by('-points')
    template = loader.get_template('quiz/index.html')
    context = {
        'best_team': best_team,
    }
    return HttpResponse(template.render(context, request))


def results(request, team_id):
    team = Team.objects.all().get(pk=team_id)
    template = loader.get_template('quiz/team.html')
    context = {
        'name': team.name,
        'points': team.points,
    }
    return HttpResponse(template.render(context, request))