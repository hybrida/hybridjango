from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import File, Subject

@login_required
def firstPage(request):
    subjects = Subject.objects.all()
    return render(request, "kok4life/firstPage.html", {"subjects":subjects})

@login_required
def filePage(request, pk):
    subject = Subject.objects.filter(pk=pk)
    files = File.objects.filter(subject=subject)
    return render(request, "kok4life/filePage.html", {"subject":subject,"files":files})
