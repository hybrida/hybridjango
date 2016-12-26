from django.shortcuts import render
from django.views import generic
from .models import Job


def index(request):
    return render(request, "jobannoucements/announcements.html",
                  {'jobs': Job.objects.all()}
                  )

class JobView(generic.DetailView):
    model = Job
    template_name = 'jobannoucements/job.html'