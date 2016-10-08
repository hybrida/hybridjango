from django.http import HttpResponse
from django.template import loader
from .models import Team


def index(request):
    best_team = Team.objects.order_by('points')[:3]
    template = loader.get_template('quiz/index.html')
    context = {
        'best_team': best_team,
    }
    return HttpResponse(template.render(context, request))


def results(request, team_id):
    response = "Du ser nå på poengene til lag %s."
    return HttpResponse(response % team_id)
