from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Course, Evaluation


def index(request):
    courses = Course.objects.filter(semester="høst")
    return render(request, 'evaluation/index.html',{"courses":courses})


def spring(request):
    courses = Course.objects.filter(semester="vår")
    return render(request, 'evaluation/våremner.html',{"courses":courses})


def evaluation(request, pk):
    course = get_object_or_404(Course, pk=pk)
    evaluations = Evaluation.objects.filter(course_id=pk)
    workload_avg = Evaluation.objects.filter(course_id=pk).aggregate(Avg('workload'))

    return render(request, 'evaluation/evaluate.html',
                  {'course': course,
                   'evaluations':evaluations,
                   'workload_avg':workload_avg,
                   }
                  )