from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import File, Subject
from .forms import KokfForm, KoksForm


def fileForm(request):
    if request.method == 'POST':
        form = KokfForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('kok:firstPage')
    else:
        form = KokfForm()
    return render(request, 'kok4life/fileForm.html', {
        'form': form
    })

def subjectForm(request):
    if request.method == 'POST':
        form = KoksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kok:firstPage')
    else:
        form = KoksForm()
        return render(request, 'kok4life/subjectForm.html', {'form':form})


@login_required
def firstPage(request):
    subjects = Subject.objects.all()
    return render(request, "kok4life/firstPage.html", {"subjects":subjects})

@login_required
def filePage(request, pk):
    subject = Subject.objects.filter(pk=pk)
    files = File.objects.filter(subject__in=subject)
    return render(request, "kok4life/filePage.html", {"subject":subject,"files":files})




