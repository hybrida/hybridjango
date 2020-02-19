from django.shortcuts import render, redirect
from .models import Evaluation
from .forms import EvaluationForm
from ..registration.models import Subject

def course_views(request):
    courses = Subject.objects.order_by('code').all()
    return render(request, 'evaluation/main_page.html', {'courses':courses})


def get_course(request, pk):
    course = Subject.objects.filter(pk=pk).first()
    evaluations = Evaluation.objects.filter(course=course).all()
    return render(request,'evaluation/course.html', {'course':course, 'evaluations':evaluations})

def get_evaluation_form(request):
        form = EvaluationForm(request.POST)
        if request.method == 'POST':
            form = EvaluationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.author = request.user
                application.profile = request.user.specialization.name
                application.save()
                course =Subject.objects.filter(pk=application.course.pk).first()
                course.number_of_evaluations = Evaluation.objects.filter(course=course).__len__()
                average = 0
                for i in Evaluation.objects.filter(course=course):
                    average += i.score
                print(Evaluation.objects.filter(course=course).__len__())

                print(average)
                course.average_score = average/(Evaluation.objects.filter(course=course).__len__())
                course.save()
                return redirect('evaluation:course_views')

        return render(request, 'evaluation/evaluation_form.html', {
            'form': form,
        })


def search(request):
    query = request.GET['search']
    result_name = Subject.objects.filter(name__icontains=query)
    result_code = Subject.objects.filter(code__icontains=query)
    from itertools import chain
    result = list(chain(result_name, result_code))
    return render(request, 'evaluation/main_page.html', {'courses':result})




