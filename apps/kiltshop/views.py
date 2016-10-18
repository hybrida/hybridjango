from django.shortcuts import render


def index(request):
    return render(request, "kiltshop/info.html")

def info2(request):
    return render(request, "kiltshop/info2.html")

def bestilling(request):
    return render(request, "kiltshop/bestilling.html")

def shop(request):
    return render(request, "kiltshop/shop.html")

def admin(request):
    return render(request, "kiltshop/admin.html")