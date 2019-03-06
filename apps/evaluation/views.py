from django.shortcuts import render
from .models import Course, Evaluation

# Create your views here.
def course_views(request):
    courses = Course.objects.all().order_by('course_code')
    return render(request, 'evaluation/main_page.html', {'courses':courses})


def get_course(request, pk):
    course = Course.objects.filter(pk=pk).first()
    evaluations = Evaluation.objects.filter(course=course).all()
    return render(request,'evaluation/course.html', {'course':course, 'evaluations':evaluations})


