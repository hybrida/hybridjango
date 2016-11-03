from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Product, Order


def index(request):
    return render(request, "kiltshop/info.html")

def order(request):
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html')
    else:
        user = request.user
        if request.method == 'POST':
            delete = request.POST.get('delete')
            order = Order.objects.filter(user=user).first()
            order.products.remove(delete)
            order.save()

        return render(request,"kiltshop/bestilling.html", {'products': Product.objects.filter(order=Order.objects.filter(user=user))})


def shop(request):
    if not request.user.is_staff: #I tilfelle noen har lyst å shoppe før release
        return render(request, 'registration/login.html')
    user = request.user
    if request.method == 'POST':
        products = request.POST.getlist('product', None)
        if not len(products) > 0:
            messages.warning(request, 'Du har ikke valgt noen produkt!') #Skal være messages.error, men den funket ikke tidligere (hadde ikke farge)
        else:
            new_kilt = False
            has_kilt = False
            new_sporra = False
            has_sporra = False
            has_kiltID = 0
            has_sporraID = 0
            kilt_numb= 0
            sporra_numb= 0
            for product in products:
                if Product.objects.get(pk=product).type == 'K':
                    kilt_numb+=1
                    new_kilt=True
                if Product.objects.get(pk=product).type == 'S':
                    sporra_numb+=1
                    new_sporra=True

            if kilt_numb > 1:
                messages.warning(request, 'Error: Du har valgt flere enn 1 kilt!')  # Skal være messages.error, men den funket ikke tidligere (hadde ikke farge)
            elif sporra_numb > 1:
                messages.warning(request, 'Error: Du har valgt mer enn 1 sporra!')  # Skal være messages.error, men den funket ikke tidligere (hadde ikke farge)
            else:
                if products is not None:
                    if Order.objects.filter(user=user).exists():
                        order = Order.objects.filter(user=user).first()
                        for product in order.products.all():
                            print("count")
                            if product.type == 'K':
                                has_kiltID=product.pk
                                has_kilt=True
                            if product.type == 'S':
                                has_sporra=True
                                has_sporraID=product.pk


                        if has_kilt and new_kilt:
                            order.products.remove(has_kiltID)

                        if has_sporra and new_sporra:
                            order.products.remove(has_sporraID)



                        order = Order.objects.filter(user=user).first()
                        order.products.add(*products)
                        order.save()
                        return HttpResponseRedirect("/kilt/bestilling")
                    else:
                        order = Order.objects.create(user=user)
                        order.products.add(*products)
                        order.save()
                        return HttpResponseRedirect("/kilt/bestilling")




    return render(request, "kiltshop/shop.html", {"products": Product.objects.all(), "kilts": Product.objects.filter(type="k")})


def admin(request):
        orders = Order.objects.all()
        return render(request, "kiltshop/admin.html", {'orders': orders})

