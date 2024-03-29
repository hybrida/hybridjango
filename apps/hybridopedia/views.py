from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.registration.models import Subject
from apps.registration.forms import SubjectForm
from .models import File
from .forms import HybridopediaFileForm


# TODO: PEP 8?
@login_required
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


@login_required
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
    context = {
        "subjects": Subject.objects.all(),
        "first": Subject.objects.filter(year="First"),
        "second": Subject.objects.filter(year="Second"),
        "third": Subject.objects.filter(year="Third"),
        "fourth": Subject.objects.filter(year="Fourth"),
        "fifth": Subject.objects.filter(year="Fifth"),
        "thirdFifth": Subject.objects.filter(year="Third-Fifth"),
        "rest": Subject.objects.filter(year="")
    }
    return render(request, "hybridopedia/firstPage.html", context)


@login_required
def filePage(request, pk):
    subject = Subject.objects.filter(pk=pk)
    files = File.objects.filter(subject__in=subject)
    return render(request, "hybridopedia/filePage.html", {"subject": subject, "files": files})
