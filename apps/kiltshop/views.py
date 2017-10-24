from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import timezone
from .models import Product, Order, ProductInfo, OrderInfo
from .forms import ProductForm, OrderInfoForm
import datetime


def index(request):
    return render(request, "kiltshop/info.html")


@login_required
def order(request):
    now = datetime.datetime.now()
    active_order = OrderInfo.objects.filter(endTime__gte=now).first()
    active=False
    if active_order:
        active = True
    user_order = Order.objects.filter(user=request.user).first()
    if request.method == 'POST':
        if 'delete_product' in request.POST:
            delete = request.POST.get('delete_product')
            m_qs = ProductInfo.objects.filter(order=user_order, product=delete)
            m = m_qs.get()
            m.delete()
        elif 'delete_comment' in request.POST:
            user_order.comment = ""
        user_order.save()
    if user_order:
        if not user_order.products.first() and not user_order.comment:
            user_order.delete()
    return render(request, "kiltshop/bestilling.html",
        {'products': Product.objects.filter(order=Order.objects.filter(user=request.user)),
        'productInfo': ProductInfo.objects.filter(order=Order.objects.filter(user=request.user).first()),
        'order': user_order, 'active': active
        }
                  )


def admin_orderoverview(request):
    if request.method == 'POST':
        if 'delete_orders' in request.POST:
            delete = request.POST.get('delete_orders')
            OrderInfo.objects.filter(pk=delete).get().delete()
        if 'edit_order' in request.POST:
            edit = request.POST.get('edit_order')
            return redirect('kilt:order_edit', edit)
        if 'show_order' in request.POST:
            show = request.POST.get('show_order')
            return redirect('kilt:order_view', show)

    return render(request, "kiltshop/order_display.html",
                {'orderinfo':  OrderInfo.objects.all(),}
    )


def order_view(request, pk):
    user_order = None
    user_products = None
    current_order = OrderInfo.objects.filter(pk=pk).get()
    all_ordered_products = ProductInfo.objects.all()
    ordered_products_in_this_period = [] #Alle bestilte produkter i den gjeldende perioden
    orders = current_order.orders.all()
    orders_pk = [] #Alle pvrivate keys til order som tilhører den gjeldende perioden
    for order in orders:
        print(order.pk)
        orders_pk.append(order.pk)

    ordered_products_numbered = []
    for product in all_ordered_products:
        print(product.order.pk)
        if product.order.pk in orders_pk:
            print('Lagt til')
            print(product.product.name)
            ordered_products_in_this_period.append(product)
            ordered_products_numbered.append([product.product.name, product.size, product.number])


    unique_ordered = []

    start = True
    for item in ordered_products_numbered:
        found = False
        if start:
            unique_ordered.append([item[0], item[1], item[2]])
            start = False
        else:
            for i in range(0, len(unique_ordered)):
                if item[0] == unique_ordered[i][0]:
                    found = True
                    if item[1] is not None and unique_ordered[i][1] is not None:
                        if item[1] == unique_ordered[i][1]:
                            unique_ordered[i][2] += item[2]
                        else:
                            new = True
                            for j in range(0, len(unique_ordered)):
                                if item[1] == unique_ordered[j][1]:
                                    new = False
                                else:
                                    pass
                            if new:
                                unique_ordered.append([item[0], item[1], item[2]])
                    else:
                        unique_ordered[i][2] += item[2]
            if not found:
                unique_ordered.append([item[0], item[1], item[2]])
    unique_ordered.sort()



    if request.method == 'POST':
        if 'showUser' in request.POST:
            user_id = request.POST.get('selected_user')
            print(user_id)
            if int(user_id) == -1:
                pass
            else:
                user_order = orders.filter(user=user_id).first()
                user_products = user_order.products.all()

        if 'change_status' in request.POST:
            put = request.POST.get('order_status')
            status = put.split(':')
            order_pk = status[1]
            status = status[0]
            user_order = Order.objects.filter(pk=order_pk).first()
            user_order.status = status
            user_order.save()
            return HttpResponseRedirect("/kilt/admin")


    return render(request, "kiltshop/order_view.html",
                  {'order':current_order,
                   'products':ordered_products_in_this_period,
                   'ordered_products':unique_ordered,
                   'orders':orders,
                   'user_order':user_order,
                   'user_products':user_products,
                   'user_productinfo': ProductInfo.objects.filter(order=user_order)}
                  )


@permission_required(['kiltshop.add_order', 'kiltshop.change_order', 'kiltshop.delete_order'])
def admin(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orderinfo = OrderInfo.objects.all()
    user_order = None
    user_products = None
    total_items = ProductInfo.objects.all() #Alle produkter som har blitt bestilt med tilhørende info, i.e. størrelse
    ordered_products = []
    for item in total_items:
        item_info = [item.product.name, item.size, item.number]
        ordered_products.append(item_info)
    unique_ordered = []
    start = True
    for item in ordered_products:
        found = False
        if start:
            unique_ordered.append([item[0], item[1], item[2]])
            start = False
        else:
            for i in range(0, len(unique_ordered)):
                    if item[0] == unique_ordered[i][0]:
                        found = True
                        if item[1] is not None and unique_ordered[i][1] is not None:
                            if item[1] == unique_ordered[i][1]:
                                unique_ordered[i][2] += item[2]
                            else:
                                new = True
                                for j in range(0, len(unique_ordered)):
                                    if item[1] == unique_ordered[j][1]:
                                        new = False
                                    else:
                                        pass
                                if new:
                                    unique_ordered.append([item[0], item[1], item[2]])
                        else:
                            unique_ordered[i][2] += item[2]
            if not found:
                unique_ordered.append([item[0], item[1], item[2]])
    unique_ordered.sort()

    if request.method == 'POST':
        if 'showUser' in request.POST:
            user_id = request.POST.get('selected_user')
            if int(user_id) == -1:
                pass
            else:
                user_order = Order.objects.filter(user=user_id).first()
                user_products = user_order.products.all()

        if 'change_status' in request.POST:
            put = request.POST.get('order_status')
            status = put.split(':')
            order_pk = status[1]
            status = status[0]
            user_order = Order.objects.filter(pk=order_pk).first()
            user_order.status = status
            user_order.save()
            return HttpResponseRedirect("/kilt/admin")

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


@permission_required(['kilt.delete_product'])
def admin_productoverview(request):
    if request.method == "POST":
        if 'delete_product' in request.POST:
            delete = request.POST.get('delete_product')
            Product.objects.filter(pk=delete).get().delete()
        if 'edit_product' in request.POST:
            edit = request.POST.get('edit_product')
            return redirect('kilt:product_edit', edit)
    return render(request, "kiltshop/admin_productoverview.html",
                  {'products': Product.objects.all()})

@permission_required(['kilt.add_product'])
def product_new(request):
    action = 'Lag nytt'
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.timestamp = timezone.now()
            product.save()
            return redirect('kilt:admin_productoverview')

    form = ProductForm(request.POST)
    return render(request, "kiltshop/product_form.html", {'action':action,'form':form })


@permission_required(['kilt.change_product'])
def product_edit(request, pk):
    action = "Rediger"
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.published_date = timezone.now()
            product.save()
            return redirect('kilt:admin_productoverview')
    else:
        form = ProductForm(instance=product)
    return render(request, "kiltshop/product_form.html", {'action':action,'form':form })

@permission_required(['kilt.add_order'])
def order_new(request):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    active_order = OrderInfo.objects.filter(endTime__gte=now).first()
    if active_order:
        active = True
    else:
        active = False
    action = 'Lag ny'
    if request.method == "POST":
        form = OrderInfoForm(request.POST)
        startTime = form['startTime'].value()
        endTime = form['endTime'].value()
        print(startTime)
        print(endTime)
        if startTime == "" or endTime == "":
            messages.warning(request, 'Ugyldig input!')
            return redirect('kilt:order_new')
        elif startTime >= endTime:
            messages.warning(request, 'Starten må være før slutten!')
            return redirect('kilt:order_new')
        elif active:
            if endTime>=str(now):
                messages.warning(request, 'Man kan kun ha et aktivt tidsrom for bestilling')
                return redirect('kilt:order_new')
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect('kilt:admin_orderoverview')

    form = OrderInfoForm(request.POST)
    return render(request, "kiltshop/order_form.html", {'action':action,'form':form })

@permission_required(['kilt.change_order'])
def order_edit(request, pk):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    active_order = OrderInfo.objects.filter(endTime__gte=now).first()
    if active_order:
        active = True
    else:
        active = False
    action = "Rediger"
    order = get_object_or_404(OrderInfo, pk=pk)
    if request.method == "POST":
        form = OrderInfoForm(request.POST, instance=order)
        startTime=form['startTime'].value()
        endTime=form['endTime'].value()
        if startTime == "" or endTime == "":
            messages.warning(request, 'Ugyldig input!')
            return redirect('kilt:order_edit', order.pk)
        elif startTime >= endTime:
            messages.warning(request, 'Starten må være før slutten!')
            return redirect('kilt:order_edit', order.pk)
        if active:
            if str(active_order.pk) == str(pk):
                pass
            elif endTime>=str(now):
                messages.warning(request, 'Man kan kun ha et aktivt tidsrom for bestilling')
                return redirect('kilt:order_edit', order.pk)

        if form.is_valid():
                order = form.save(commit=False)
                order.save()
                return redirect('kilt:admin_orderoverview')

    form = OrderInfoForm(instance=order)
    return render(request, "kiltshop/order_form.html", {'action':action,'form':form })

@login_required
def shop(request):
    user = request.user
    types = Product.type_choices
    now = datetime.datetime.now()
    active_order = OrderInfo.objects.filter(endTime__gte=now).first()
    active=False
    if active_order:
        active=True
    if request.method == 'POST':
        products = request.POST.getlist('product_k', None)
        products += request.POST.getlist('product_s', None)
        products += request.POST.getlist('product_e', None)
        comment = request.POST.get('comment', None)

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
                   'types':types,
                   'order': Order.objects.filter(user=user).first(),
                   'active':active
                   })
