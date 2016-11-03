from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Product, Order, ProductInfo


def index(request):
    return render(request, "kiltshop/info.html")


def order(request):

    if not request.user.is_authenticated():
        return render(request, 'registration/login.html')
    else:
        user_order = Order.objects.filter(user=request.user).first()
        if request.method == 'POST':
            delete = request.POST.get('delete')
            user_order.products.remove(delete)
            user_order.save()

        return render(request,"kiltshop/bestilling.html",
            {'products': Product.objects.filter(order=Order.objects.filter(user=request.user)),
             'productInfo': ProductInfo.objects.filter(order=Order.objects.filter(user=request.user).first()),
             'order': user_order}
        )


def shop(request):
    if not request.user.is_staff:  # In case somebody unwanted starts "shopping"
        return render(request, 'registration/login.html')
    user = request.user
    if request.method == 'POST':
        products = request.POST.getlist('product', None)
        size = request.POST.get('size', None)
        number = request.POST.get('number', None)
        print(number)
        print(size)
        if not len(products) > 0:
            messages.warning(request, 'Ingen produkter er valgt.')
        else:
            new_kilt = False
            has_kilt = False
            new_sporra = False
            has_sporra = False
            has_kilt_id = 0
            has_sporra_id = 0
            kilt_number = 0
            sporra_number = 0
            for product in products:
                if Product.objects.get(pk=product).type == 'K':
                    kilt_number += 1
                    new_kilt = True
                if Product.objects.get(pk=product).type == 'S':
                    sporra_number += 1
                    new_sporra = True

            if kilt_number > 1:
                messages.warning(request, 'Du har valgt mer enn en kilt.')
            elif sporra_number > 1:
                messages.warning(request, 'Du har valgt mer enn en sporra.')
            else:
                if products is not None:
                    if Order.objects.filter(user=user).exists():
                        order_list = Order.objects.filter(user=user).first()
                        for product in order_list.products.all():
                            if product.type == 'K':
                                has_kilt_id = product.pk
                                has_kilt = True
                            if product.type == 'S':
                                has_sporra=True
                                has_sporra_id=product.pk

                        if has_kilt and new_kilt:
                            order_list.products.remove(has_kilt_id)

                        if has_sporra and new_sporra:
                            order_list.products.remove(has_sporra_id)

                        comment = request.POST.get('comment', None)
                        order_list = Order.objects.filter(user=user).first()
                        if len(comment) > 0:
                            order_list.comment = comment

                        order_list.products.add(*products)
                        order_list.save()
                        return HttpResponseRedirect("/kilt/bestilling")
                    else:
                        order_list = Order.objects.create(user=user)
                        comment = request.POST.get('comment', None)
                        order_list.comment = comment
                        order_list.products.add(*products) # ignore this
                        order_list.save()
                        return HttpResponseRedirect("/kilt/bestilling")

    return render(request, "kiltshop/shop.html", {"products": Product.objects.all(), "kilts": Product.objects.filter(type="k")})


def admin(request):
        orders = Order.objects.all()
        return render(request, "kiltshop/admin.html", {'orders': orders})

