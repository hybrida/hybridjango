from django.shortcuts import render


def index(request):
    return render(request, "kiltbestilling/info.html")

def bestilling(request):
    return render(request, "kiltbestilling/bestilling.html")

def shop(request):
    return render(request, "kiltbestilling/shop.html")

def admin(request):
    return render(request, "kiltbestilling/admin.html")