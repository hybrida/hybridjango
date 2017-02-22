from django.shortcuts import render

def index(request):
    return render(request, "staticpages/search.html")