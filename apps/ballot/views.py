from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.rfid.models import GeneralAssembly
from hybridjango.utils import group_test


class Ballot:
    nr = 0
    title = 'Avstemning'
    choices = [
        'Blank',
        'Vevkom',
        'Bedkom',
        'Arrkom',
        'Jentekom',
        'Redaksjonen',
    ]
    only_members = True
    empty_votes = True
    is_attending = True
    has_voted = []
    votes = []
    active = True

class Suggestion:
    num = 0
    author = "Ikke vevsjef"
    suggestion_text = "Vevkom burde ta over styret"
    suggestions_enabled = False



empty_vote = 'Tomt'
suggestion_list = []

@user_passes_test(group_test("Tellekorps"))
def overview(request):
    user = request.user
    if request.method == 'POST':
        if 'ballot_form' in request.POST:
            Ballot.title = request.POST.get('title', 'Avstemning')
            Ballot.only_members = True if request.POST.get('membersOnly') else False
            Ballot.empty_votes = True if request.POST.get('empty_votes') else False
            Ballot.is_attending = True if request.POST.get('is_attending') else False
            Ballot.choices = [v for k, v in request.POST.items() if k.startswith('choice-')]
            Ballot.votes = []
            Ballot.has_voted = []
            Ballot.nr += 1
        return HttpResponseRedirect('#')
    elif 'active' in request.GET:
        Ballot.active = not (request.GET['active'] == 'Deaktiver')
    return render(
        request, 'ballot/overview.html', context={
            'active': Ballot.active,
            },
        )

@user_passes_test(group_test("Nestleder"))
def suggestion_overview(request):
    user = request.user
    if request.method == 'POST':
        if 'toggle_suggestions' in request.POST:
            Suggestion.suggestions_enabled = not Suggestion.suggestions_enabled
        elif 'clear_suggestions' in request.POST:
            del suggestion_list[:]
        return HttpResponseRedirect("#")

    return render(request, 'ballot/suggestions.html', context={
            'suggestions_enabled' : Suggestion.suggestions_enabled
    })

@login_required
def post_suggestion(request):
    sugg = Suggestion()
    sugg.num += 1
    sugg.author = request.user
    sugg.suggestion_text = request.POST.get('suggestion_text')
    suggestion_list.append(sugg)

@user_passes_test(group_test("Nestleder"))
def get_suggestions(request):
    json_list = [{
        "author_name" : suggestion.author.full_name,
        "suggestion_text" : suggestion.suggestion_text,
    } for suggestion in suggestion_list]
    return JsonResponse({"suggestion_list" : json_list})


@login_required
def ballot(request):
    return render(request, 'ballot/voteview.html', get_ballot_dict(request.user))


@login_required
def get_choices(request):
    return JsonResponse(get_ballot_dict(request.user))


def get_ballot_dict(user):
    choices = Ballot.choices.copy()
    if Ballot.empty_votes:
        choices.append(empty_vote)
    return {
        'nr': Ballot.nr,
        'title': Ballot.title,
        'choices': choices,
        'has_voted': user.pk in Ballot.has_voted,
        'active': Ballot.active,
        'suggestions_enabled' : Suggestion.suggestions_enabled,
    }


def vote(request):
    if request.method == 'POST':
        user = request.user
        generalassembly = GeneralAssembly.objects.all().last() #fetches the newest made generalassembly object

        if not user.is_authenticated:
            return HttpResponse("Du må være innlogget for å stemme")
        if not Ballot.active:
            return HttpResponse("Avstemningen er ikke aktiv")
        if user.pk < 2:
            return HttpResponse("Linjeforeningen Hybrida kan ikke stemme selv")
        if Ballot.only_members and not user.member:
            return HttpResponse("Kun medlemmer kan stemme")
        if Ballot.is_attending and user not in generalassembly.users.all():
            return HttpResponse("Du må registrere oppmøte for å kunne stemme")
        if user.pk in Ballot.has_voted:
            return HttpResponse("Du har allerede stemt")

        new_vote = request.POST.get("choice", None)
        if new_vote in Ballot.choices or (Ballot.empty_votes and new_vote == empty_vote):
            Ballot.has_voted.append(user.pk)
            Ballot.votes.append(new_vote)
            return HttpResponse("Du stemte på {}.".format(new_vote))

    return HttpResponse("Du avga ingen stemme")

@user_passes_test(group_test("Tellekorps"))
def get_results(request):
    user = request.user
    if not (user.is_authenticated and group_test("Tellekorps")):
        return JsonResponse(
            {"title": "Hvem er best?", "results": [{"name": "vevkom", "votes": 9001}, {"name": "andre", "votes": 0}],
             "total": 9001, "total_nonblank": 9001})
    results = [{'name': choice, 'votes': Ballot.votes.count(choice)} for choice in Ballot.choices]
    total_nonblank = total = len(Ballot.votes)
    if Ballot.empty_votes:
        results.append({'name': empty_vote, 'votes': Ballot.votes.count(empty_vote)})
        total_nonblank -= Ballot.votes.count(empty_vote)
    return JsonResponse({'title': Ballot.title, 'results': results, 'total': total, 'total_nonblank': total_nonblank})
