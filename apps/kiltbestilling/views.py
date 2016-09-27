from django.shortcuts import render


def index(request):
    return render(request, "kiltbestilling/test.html")

def bestilling(request):
    return render(request, "kiltbestilling/bestilling.html")