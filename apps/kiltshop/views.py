from django.shortcuts import render


def index(request):
    return render(request, "kiltshop/info.html")

def bestilling(request):
    return render(request, "kiltshop/bestilling.html")