from django.shortcuts import render
from apps.interestgroups.models import *
# Create your views here.

def hybridaFK(request):
    return render(request, "internside/internside.html")