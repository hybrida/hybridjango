from django.shortcuts import render
from .models import Ridder

# Create your views here.

def index(request):
    context ={'Ridder': Ridder.objects.all()}
    print(context)
    print("asdf")
    return render(request, "griffensorden/griffens_orden.html",
                  context=context
                  )