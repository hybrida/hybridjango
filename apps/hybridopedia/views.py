from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.registration.models import Subject
from apps.registration.forms import SubjectForm
from .models import File
from .forms import HybridopediaFileForm


# TODO: Login required for forms?
# TODO: PEP 8?
def fileForm(request):
    if request.method == 'POST':
        form = HybridopediaFileForm(request.POST, request.FILES)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
            return redirect('hybridopedia:firstPage')
    else:
        form = HybridopediaFileForm()
    return render(request, 'hybridopedia/fileForm.html', {
        'form': form
    })


def subjectForm(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
            return redirect('hybridopedia:firstPage')
    else:
        form = SubjectForm()
        return render(request, 'hybridopedia/subjectForm.html', {'form': form})


@login_required
def firstPage(request):
    subjects = Subject.objects.all()
    return render(request, "hybridopedia/firstPage.html", {"subjects": subjects})


@login_required
def filePage(request, pk):
    subject = Subject.objects.filter(pk=pk)
    files = File.objects.filter(subject__in=subject)
    return render(request, "hybridopedia/filePage.html", {"subject": subject, "files": files})
