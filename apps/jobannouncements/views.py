from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from .models import Job
from .forms import JobForm
import datetime
from django.utils import timezone
from django.shortcuts import redirect


def index(request):
    now = datetime.datetime.now()
    status = "Aktive"
    return render(request, "jobannoucements/announcements.html",
                  {'status':status,'priorities': Job.objects.filter(deadline__gte=now).order_by('-weight', 'deadline').filter(priority=1),
                   'jobs': Job.objects.filter(deadline__gte=now).order_by('-weight','deadline').filter(priority=0),
                   'job_list':Job.objects.filter(deadline__gte=datetime.datetime.now()).order_by('deadline')})


def job_previous(request):
    now = datetime.datetime.now()
    status = "Tidligere"
    return render(request, "jobannoucements/announcements.html",
                  {'status':status,'jobs': Job.objects.filter(deadline__lte=now).order_by('-deadline'),'job_list':Job.objects.filter(deadline__gte=datetime.datetime.now()).order_by('deadline')})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobannoucements/job.html', {'job': job})


@permission_required(['jobannoucements.add_job'])
def new_job(request):
    action = 'Lag ny'
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.author = request.user
            job.timestamp = timezone.now()
            job.save()
            return redirect('jobs:job_detail', pk=job.pk)

    form = JobForm(request.POST)
    return render(request, "jobannoucements/job_form.html", {'action':action,'form':form,'job_list':Job.objects.filter(deadline__gte=datetime.datetime.now()).order_by('deadline') })


@permission_required(['jobannoucements.change_job'])
def job_edit(request, pk):
    action = "Rediger"
    job = get_object_or_404(Job, pk=pk)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            job.author = request.user
            job.published_date = timezone.now()
            job.save()
            return redirect('jobs:job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, "jobannoucements/job_form.html", {'action':action,'form':form,'job_list':Job.objects.filter(deadline__gte=datetime.datetime.now()).order_by('deadline') })


@permission_required(['jobannoucements.delete_job'])
def JobAdmin(request):
    if request.method == "POST":
        if 'delete_job' in request.POST:
            delete = request.POST.get('delete_job')
            Job.objects.filter(pk=delete).get().delete()
        if 'edit_job' in request.POST:
            edit = request.POST.get('edit_job')
            return redirect('jobs:job_edit', edit)
    return render(request, "jobannoucements/job_admin.html",
                  {'jobs': Job.objects.all().order_by('deadline').reverse(),'job_list':Job.objects.filter(deadline__gte=datetime.datetime.now()).order_by('deadline')})

