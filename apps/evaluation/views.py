from django.shortcuts import render
from .models import Course

# Create your views here.
def course_views(request):
    courses = Course.objects.all().order_by('course_code')
    return render(request, 'evaluation/main_page.html', {'courses':courses})


