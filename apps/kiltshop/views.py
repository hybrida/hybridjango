from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Product, Order, ProductInfo, OrderInfo


def index(request):
    return render(request, "kiltshop/info.html")

@login_required
def order(request):
        active_order = OrderInfo.objects.filter(status=True).first()
        if active_order:
            active = True
        else:
            active = False
        user_order = Order.objects.filter(user=request.user).first()
        if request.method == 'POST':
            delete = request.POST.get('delete')
            m_qs = ProductInfo.objects.filter(order=user_order, product=delete)
            m = m_qs.get()
            m.delete()

            if len(user_order.products.all()) == 0:
                user_order.delete()
            else:
                user_order.save()

        return render(request,"kiltshop/bestilling.html",
            {'products': Product.objects.filter(order=Order.objects.filter(user=request.user)),
             'productInfo': ProductInfo.objects.filter(order=Order.objects.filter(user=request.user).first()),
             'order': user_order, 'activated': active}
        )


@login_required
def shop(request):
    user = request.user
    active_order = OrderInfo.objects.filter(status=True).first()
    if active_order:
        active = True
    else:
        active = False
    if request.method == 'POST':
        products = request.POST.getlist('product_k', None)
        products += request.POST.getlist('product_s', None)
        products += request.POST.getlist('product_e', None)

        if not len(products) > 0:
            messages.warning(request, 'Ingen produkter er valgt.')
        else:
            new_kilt = False
            has_kilt = False
            new_sporra = False
            has_sporra = False
            has_kilt_id = 0
            has_sporra_id = 0
            for product in products:
                if Product.objects.get(pk=product).type == 'K':
                    new_kilt = True
                if Product.objects.get(pk=product).type == 'S':
                    new_sporra = True
            else:
                if products is not None:
                    if Order.objects.filter(user=user).exists():
                        order_list = Order.objects.filter(user=user).first()
                        for product in order_list.products.all():
                            if product.type == 'K':
                                has_kilt_id = product.pk
                                has_kilt = True
                            if product.type == 'S':
                                has_sporra = True
                                has_sporra_id = product.pk
                            if product.type == 'E':
                                for item in products:
                                    if str(item) == str(product.pk):
                                        m_qs = ProductInfo.objects.filter(order=order_list, product=item)
                                        m = m_qs.get()
                                        m.delete()

                        if has_kilt and new_kilt:
                            m_qs = ProductInfo.objects.filter(order=order_list, product=has_kilt_id)
                            m = m_qs.get()
                            m.delete()

                        if has_sporra and new_sporra:
                            m_qs = ProductInfo.objects.filter(order=order_list, product=has_sporra_id)
                            m = m_qs.get()
                            m.delete()

                        comment = request.POST.get('comment', None)
                        order_list = Order.objects.filter(user=user).first()
                        if comment:
                            order_list.comment = comment

                        for product in products:
                            number = int(request.POST.get('number-{id}'.format(id=product), 1))
                            if number > 0:
                                size = request.POST.get('size-{id}'.format(id=product), None)
                                item = Product.objects.get(pk=product)
                                productinfo = ProductInfo(order=order_list, product=item, size=size, number=number)
                                productinfo.save()
                        order_list.save()
                        active_order.save()
                        return HttpResponseRedirect("/kilt/bestilling")
                    else:
                        order_list = Order.objects.create(user=user)
                        comment = request.POST.get('comment', None)
                        order_list.comment = comment
                        for product in products:
                            number = int(request.POST.get('number-{id}'.format(id=product), 1))
                            if number > 0:
                                size = request.POST.get('size-{id}'.format(id=product), None)
                                item = Product.objects.get(pk=product)
                                productinfo = ProductInfo(order=order_list, product=item, size=size, number=number)
                                productinfo.save()
                        order_list.save()
                        active_order.orders.add(order_list)
                        active_order.save()
                        return HttpResponseRedirect("/kilt/bestilling")

    return render(request, "kiltshop/shop.html", {"products": Product.objects.all(),'activated': active})


def admin(request):
    user_order = Order.objects.all()
    products = Product.objects.all()
    orderinfo = OrderInfo.objects.all()

    return render(request, "kiltshop/admin.html",
                  {'products': products,
                   'orders': user_order,
                  'orderinfo': orderinfo},
                  )