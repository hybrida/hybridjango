from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Job
from .forms import JobForm
from django.utils import timezone
from django.shortcuts import redirect


def index(request):
    return render(request, "jobannoucements/announcements.html",
                  {'jobs': Job.objects.filter()})


def job_all(request):
    return render(request, "jobannoucements/announcements.html",
                  {'jobs': Job.objects.all()}
                  )


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobannoucements/job.html', {'job': job})


def new_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.author = request.user
            job.timestamp = timezone.now()
            job.save()
            return redirect(index(request))

    form = JobForm(request.POST)
    return render(request, "jobannoucements/job_form.html", {'form':form })


def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            job.author = request.user
            job.published_date = timezone.now()
            job.save()
            return redirect('job_detail', pk=47)
    else:
        form = JobForm(instance=job)
    return render(request, "jobannoucements/job_form.html", {'form':form })


def JobAdmin(request):
    if request.method == "POST":
        if 'delete_job' in request.POST:
            delete = request.POST.get('delete_job')
            Job.objects.filter(pk=delete).get().delete()
    return render(request, "jobannoucements/job_admin.html",
                  {'jobs': Job.objects.all(), })

