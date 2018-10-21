from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import File, Subject
from .forms import KokfForm, KoksForm

@login_required
def firstPage(request):
    subjects = Subject.objects.all()
    return render(request, "kok4life/firstPage.html", {"subjects":subjects})

@login_required
def filePage(request, pk):
    subject = Subject.objects.filter(pk=pk)
    files = File.objects.filter(subject__in=subject)
    return render(request, "kok4life/filePage.html", {"subject":subject,"files":files})

def fileForm(request):
    action =1    #  når knappen trykkes

    if request.method == 'POST':
        form = KokfForm(request.POST, request.FILES)
        if form.is_valid() & action:

            return render(request, 'kok4life/fileForm.html', {'form': form, 'action':action})
    else:
        form = KokfForm()
    return render(request, 'kok4life/fileForm.html', {'form': form, 'action':action})



