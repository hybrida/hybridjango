from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Product, Order, ProductInfo, OrderInfo
import datetime


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
        if len(user_order.products.all()) == 0 and not user_order.comment:
            user_order.delete()
        else:
            user_order.save()
        if request.method == 'POST':
            if 'delete_product' in request.POST:
                delete = request.POST.get('delete_product')
                m_qs = ProductInfo.objects.filter(order=user_order, product=delete)
                m = m_qs.get()
                m.delete()

            elif 'delete_comment' in request.POST:
                delete = request.POST.get('delete_comment')
                user_order.comment = ""
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
        comment = request.POST.get('comment', None)
        print(len(comment))
        print(len(products))

        if not len(products) > 0 and not len(comment) > 0:
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

    return render(request, "kiltshop/shop.html",
                  {"products": Product.objects.all(),
                   'activated': active,
                   "order": Order.objects.filter(user=user).first()
                   })


@permission_required(['kiltshop.add_order', 'kiltshop.change_order', 'kiltshop.delete_order'])
def admin(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orderinfo = OrderInfo.objects.all()
    user_order = None
    user_products = None
    total_items = ProductInfo.objects.all()
    ordered_products = []
    for item in total_items:
        item_info = [item.product.name, item.size, item.number]
        ordered_products.append(item_info)
    unique_ordered = []
    start = True
    for item in ordered_products:
        found = False
        foundsize = False
        if start:
            unique_ordered.append([item[0],item[1],item[2]])
            start = False
        else:
            for i in range(0, len(unique_ordered)):
                    if item[0] == unique_ordered[i][0]:
                        found = True
                        if item[1] is not None and unique_ordered[i][1] is not None: #Hvis det er en gjenstand med størrelse
                            if item[1] == unique_ordered[i][1]: #Hvis størrelsen er lik
                                unique_ordered[i][2] += item[2]
                            else:
                                new = True
                                for i in range(0, len(unique_ordered)):
                                    if item[1] == unique_ordered[i][1]:
                                        new = False
                                    else:
                                        pass
                                if new:
                                    unique_ordered.append([item[0], item[1], item[2]])
                        else:
                            unique_ordered[i][2] += item[2]
            if not found:
                unique_ordered.append([item[0],item[1],item[2]])
    unique_ordered.sort()

    if request.method == 'POST':
        if 'showUser' in request.POST:
            user_id = request.POST.get('selected_user')
            if int(user_id) == -1:
                pass
            else:
                user_order = Order.objects.filter(user=user_id).first()
                user_products = user_order.products.all()

        if 'createTime' in request.POST:
            start = request.POST.get('start')
            slutt = request.POST.get('slutt')
            split_s = start.split("-")
            start_year = split_s[0]
            start_month = split_s[1]
            split_e = slutt.split("-")
            end_year = split_e[0]
            end_month = split_e[1]
            split_s = split_s[2].split(" ")
            start_day = split_s[0]
            split_e = split_e[2].split(" ")
            end_day = split_e[0]
            split_s = split_e[1].split(":")
            start_hour = split_s[0]
            start_minute = split_s[1]
            split_e = split_e[1].split(":")
            end_hour = split_s[0]
            end_minute = split_s[1]
            now = datetime.datetime.now()
            print(now.year)
            if OrderInfo.objects.filter(status=True).first():
                messages.warning(request, 'Du kan kun ha en aktiv tidsperiode om gangen, dette kan endres på hybrida.no/admin')
            else:
                OrderInfo.objects.create(startTime=start,endTime=slutt)

    return render(request, "kiltshop/admin.html", {
        'products': products,
        'orders': orders,
        'orderinfo': orderinfo,
        'total_items': total_items,
        'user_products': user_products,
        'ordered_products': unique_ordered,
        'user_productinfo': ProductInfo.objects.filter(order=user_order),
        'user_order': user_order},
      )