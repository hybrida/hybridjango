from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect


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
    has_voted = []
    votes = []


empty_vote = 'Tomt'


@login_required
def overview(request):
    user = request.user
    if not user.username == 'simennje':
        return redirect('login')
    if request.method == 'POST':
        Ballot.title = request.POST.get('title', 'Avstemning')
        Ballot.only_members = request.POST.get('membersOnly', True)
        Ballot.choices = [v for k, v in request.POST.items() if k.startswith('choice-')]
        Ballot.votes = []
        Ballot.has_voted = []
        Ballot.nr += 1
    return render(request, 'ballot/overview.html')


@login_required
def ballot(request):
    choices = Ballot.choices
    if Ballot.empty_votes:
        choices.append(empty_vote)
    context = {'choices': choices, 'title': Ballot.title, 'nr': Ballot.nr}
    return render(request, 'ballot/voteview.html', context=context)


def vote(request):
    if request.method == 'POST':
        user = request.user

        if not user.is_authenticated:
            return HttpResponse("Du må være innlogget for å stemme")
        if user.pk < 2:
            return HttpResponse("Linjeforeningen Hybrida kan ikke stemme selv")
        if Ballot.only_members and not user.member:
            return HttpResponse("Kun medlemmer kan stemme")
        if user.pk in Ballot.has_voted:
            return HttpResponse("Du har allerede stemt")

        new_vote = request.POST.get("choice", None)
        if new_vote in Ballot.choices or (Ballot.empty_votes and new_vote == empty_vote):
            Ballot.has_voted.append(user.pk)
            Ballot.votes.append(new_vote)
            return HttpResponse("Du stemte på {}.".format(new_vote))

    return HttpResponse("Du avga ingen stemme")


def get_choices(request):
    return JsonResponse({'nr': Ballot.nr, 'title': Ballot.title, 'choices': Ballot.choices})


def get_results(request):
    user = request.user
    if not (user.is_authenticated and user.username == 'simennje'):
        return JsonResponse(
            {"title": "Hvem er best?", "results": [{"name": "vevkom", "votes": 9001}, {"name": "andre", "votes": 0}],
             "total": 9001})
    results = [{'name': choice, 'votes': Ballot.votes.count(choice)} for choice in Ballot.choices]
    total_nonblank = total = len(Ballot.votes)
    if Ballot.empty_votes:
        results.append({'name': empty_vote, 'votes': Ballot.votes.count(empty_vote)})
        total -= Ballot.votes.count(empty_vote)
    return JsonResponse({'title': Ballot.title, 'results': results, 'total': total, 'total_nonblank': total_nonblank})
