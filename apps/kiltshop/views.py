from django.shortcuts import render
from .models import Product, Order


def index(request):
    return render(request, "kiltshop/info.html")

def info2(request):
    return render(request, "kiltshop/info2.html")


def order(request):
    if not request.user.is_authenticated():
        return render(request, 'accounts/login.html')
    else:
        user = request.user
        order = Order.objects.filter(user=user)
        products = Product.objects.filter(order=order)
        return render(request, "kiltshop/bestilling.html", {'products': products})


def shop(request):
    products = Product.objects.all()
    return render(request, "kiltshop/shop.html", {'products': products})


def admin(request):
    return render(request, "kiltshop/admin.html")