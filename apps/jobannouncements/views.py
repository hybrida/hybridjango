from django.shortcuts import render
from django.views import generic
from .models import Job
from .forms import JobForm
from apps.bedkom.models import Company
from django.utils import timezone
from django.shortcuts import redirect

def index(request):
    return render(request, "jobannoucements/announcements.html",
                  {'jobs': Job.objects.all()}
                  )

class JobView(generic.DetailView):
    model = Job
    template_name = 'jobannoucements/job.html'


def CreateJob(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.author = request.user
            job.timestamp = timezone.now()
            job.save()
            return redirect('/stillingsutlysninger/', pk=job.pk)
    else:
        form = JobForm()
    return render(request, "jobannoucements/job_form.html",
                  {'companies': Company.objects.all(),'form':form }
                  )

def JobAdmin(request):
    return render(request, "jobannoucements/job_admin.html",
                  {'jobs': Job.objects.all(), }
                  )

