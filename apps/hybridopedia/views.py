from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.registration.models import Subject
from apps.registration.forms import SubjectForm
from .models import File
from .forms import HybridopediaFileForm


# TODO: PEP 8?
@login_required
def file_form(request):
    if request.method == 'POST':
        form = HybridopediaFileForm(request.POST, request.FILES)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
            return redirect('hybridopedia:firstPage')
        else:
            return render(request, 'hybridopedia/fileForm.html', {'form': form})
    else:
        form = HybridopediaFileForm()
    return render(request, 'hybridopedia/fileForm.html', {'form': form})


@login_required
def subject_form(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
            return redirect('hybridopedia:firstPage')
        else:
            return render(request, 'hybridopedia/subjectForm.html', {'form': form})
    else:
        form = SubjectForm()
        return render(request, 'hybridopedia/subjectForm.html', {'form': form})


@login_required
def first_page(request):
    subjects = Subject.objects.all()
    return render(request, "hybridopedia/firstPage.html", {"subjects": subjects})


@login_required
def file_page(request, pk):
    subject = Subject.objects.filter(pk=pk)
    files = File.objects.filter(subject__in=subject)
    return render(request, "hybridopedia/filePage.html", {"subject": subject, "files": files})
