from django.shortcuts import render

from .models import Product, Order


def index(request):
    return render(request, "kiltshop/info.html")

def info2(request):
    return render(request, "kiltshop/info2.html")


def order(request):
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html')
    else:
        user = request.user
        orders = Order.objects.filter(user=user)
        products = Product.objects.filter(order=orders)
        return render(request, "kiltshop/bestilling.html", {'products': products})


def shop(request):
    return render(request, "kiltshop/shop.html", {"products": Product.objects.all(), "kilts": Product.objects.filter(type="k")})


def admin(request):
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html')
    else:
        user = request.user
        orders = Order.objects.filter(user=user)
        products = Product.objects.filter(order=orders)
        return render(request, "kiltshop/admin.html", {'products': products})