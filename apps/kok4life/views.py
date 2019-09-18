from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import File, Subject
from .forms import KokFileForm, KokSubjectForm


# TODO: Login required for forms?
# TODO: PEP 8?
def fileForm(request):
    if request.method == 'POST':
        form = KokFileForm(request.POST, request.FILES)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
            return redirect('kok:firstPage')
    else:
        form = KokFileForm()
    return render(request, 'kok4life/fileForm.html', {
        'form': form
    })


def subjectForm(request):
    if request.method == 'POST':
        form = KokSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kok:firstPage')
    else:
        form = KokSubjectForm()
        return render(request, 'kok4life/subjectForm.html', {'form': form})


@login_required
def firstPage(request):
    subjects = Subject.objects.all()
    return render(request, "kok4life/firstPage.html", {"subjects": subjects})


@login_required
def filePage(request, pk):
    subject = Subject.objects.filter(pk=pk)
    files = File.objects.filter(subject__in=subject)
    return render(request, "kok4life/filePage.html", {"subject": subject, "files": files})
