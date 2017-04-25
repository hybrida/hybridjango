from django.shortcuts import render

# Create your views here.
def eventcalendar(request):
    return render(request, "eventcalendar/ecalendar.html", )
