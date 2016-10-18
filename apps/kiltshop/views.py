from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Order


def index(request):
    return render(request, "kiltshop/info.html")

def info2(request):
    return render(request, "kiltshop/info2.html")

def bestilling(request):
    return render(request, "kiltshop/bestilling.html")

def shop(request):
    products = Product.objects.all()
    return render(request, "kiltshop/shop.html", {'products': products})





def admin(request):
    return render(request, "kiltshop/admin.html")