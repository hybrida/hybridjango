from django.shortcuts import render, redirect
from .models import Course, Evaluation
from .forms import EvaluationForm
# Create your views here.
def course_views(request):
    courses = Course.objects.all().order_by('course_code')
    return render(request, 'evaluation/main_page.html', {'courses':courses})


def get_course(request, pk):
    course = Course.objects.filter(pk=pk).first()
    evaluations = Evaluation.objects.filter(course=course).all()
    return render(request,'evaluation/course.html', {'course':course, 'evaluations':evaluations})

def get_evaluation_form(request):
        form = EvaluationForm(request.POST)
        if request.method == 'POST':
            form = EvaluationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.author = request.user
                application.save()
                course =Course.objects.filter(pk=application.course.pk).first()
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

