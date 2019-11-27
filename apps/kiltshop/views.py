from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import Product, Order, ProductInfo, OrderPeriod
from .forms import ProductForm, OrderPeriodForm
from .utils import create_excel
from collections import Counter
import datetime


def index(request):
    return render(request, "kiltshop/info.html")


@login_required
def show_order(request):
    # all orders for this user
    user_orders = Order.objects.filter(user=request.user).order_by('-pk')
    # the order to display
    shown_order = user_orders.first()
    if request.method == 'POST':
        # changes the shown order to the one selected on list
        if 'showOrder' in request.POST:
            order_id = request.POST.get('selected_order')
            if int(order_id) != -1:
                shown_order = Order.objects.get(pk=order_id)
        # deletes selected product from order
        if 'delete_product' in request.POST:
            product_id = request.POST.get('delete_product')
            product = ProductInfo.objects.get(order=shown_order, product=product_id)
            product.delete()
        # deletes comment from order
        elif 'delete_comment' in request.POST:
            shown_order.comment = ""
        shown_order.save()
    if shown_order:
        # delete order if it is empty
        if not shown_order.products.first() and not shown_order.comment:
            shown_order.delete()

    return render(request, "kiltshop/bestilling.html", {
        'product_infos': shown_order.productinfo_set.all(),
        'order': shown_order,
        'user_orders': user_orders
    })


@permission_required(['kiltshop.change_orderperiod'])
def period_overview(request):
    if request.method == 'POST':
        if 'edit_period' in request.POST:
            edit = request.POST.get('edit_period')
            return redirect('kilt:order_edit', edit)
        if 'show_period' in request.POST:
            show = request.POST.get('show_period')
            return redirect('kilt:order_view', show)
        if 'download_period' in request.POST:
            download = request.POST.get('download_period')
            return redirect('kilt:download_as_excel', download)

    return render(request, "kiltshop/order_display.html", {
        'periods':  OrderPeriod.objects.all()
    })


@permission_required(['kiltshop.change_orderperiod'])
def download_period_as_excel(request, pk):
    file = create_excel(pk)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format('kiltbestilling.xls')
    file.save(response)
    return response


# shows order for a period, with a count for each product + size combination
# can also display a single order and change payment status
@permission_required(['kiltshop.add_order', 'kiltshop.change_order', 'kiltshop.delete_order'])
def orders_in_period(request, pk):
    user_order = None
    period = OrderPeriod.objects.get(pk=pk)
    orders = period.orders.all()

    # we want to create a list of tuples of the form (name, size, count) for each combination of product and size
    # first, get a list of tuples of the form (name, size)
    unique_ordered = ProductInfo.objects.filter(order__period=period).values_list('product__name', 'size')
    # we use the built-in Counter to get a dict on the form {tuple: count}
    unique_ordered = Counter(unique_ordered)
    # finally, transform the dict to a list of tuples of with the desired form
    unique_ordered = [(*product, count) for product, count in unique_ordered.items()]
    unique_ordered.sort()

    if request.method == 'POST':
        # show a single order
        if 'showUser' in request.POST:
            user_id = request.POST.get('selected_user')
            if int(user_id) != -1:
                user_order = orders.filter(user=user_id).first()

        # change payment status of selected order
        if 'change_status' in request.POST:
            put = request.POST.get('order_status')
            status, order_pk = put.split(':')
            order = Order.objects.get(pk=order_pk)
            order.status = status
            order.save()
            return HttpResponseRedirect("/kilt/admin")

    return render(request, "kiltshop/order_view.html", {
        'period': period,
        'ordered_products': unique_ordered,
        'orders': orders,
        'user_order': user_order,
        'user_productinfos': ProductInfo.objects.filter(order=user_order)
    })


@permission_required(['kiltshop.delete_product'])
def product_overview(request):
    if request.method == "POST":
        if 'delete_product' in request.POST:
            delete = request.POST.get('delete_product')
            Product.objects.get(pk=delete).delete()
        if 'edit_product' in request.POST:
            edit = request.POST.get('edit_product')
            return redirect('kilt:product_edit', edit)
    return render(request, "kiltshop/admin_productoverview.html", {
        'products': Product.objects.all()
    })

@permission_required(['kiltshop.add_product'])
def product_new(request):
    action = 'Lag nytt'
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.timestamp = timezone.now()
            product.save()
            return redirect('kilt:product_overview')

    form = ProductForm(request.POST)
    return render(request, "kiltshop/product_form.html", {'action':action,'form':form })


@permission_required(['kiltshop.change_product'])
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
            return redirect('kilt:product_overview')
    else:
        form = ProductForm(instance=product)
    return render(request, "kiltshop/product_form.html", {'action':action,'form':form })

@permission_required(['kiltshop.add_order'])
def order_new(request):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    active_order = OrderPeriod.objects.filter(end_time__gte=now).first()
    if active_order:
        active = True
    else:
        active = False
    action = 'Lag ny'
    if request.method == "POST":
        form = OrderPeriodForm(request.POST)
        startTime = form['start_time'].value()
        endTime = form['end_time'].value()
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
                messages.warning(request, 'Man kan kun ha et tidsrom for bestilling frem i tid')
                return redirect('kilt:order_new')
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect('kilt:period_overview')

    form = OrderPeriodForm(request.POST)
    return render(request, "kiltshop/order_form.html", {'action':action,'form':form })

@permission_required(['kiltshop.change_order'])
def order_edit(request, pk):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    active_order = OrderPeriod.objects.filter(end_time__gte=now).first()
    if active_order:
        active = True
    else:
        active = False
    action = "Rediger"
    order = get_object_or_404(OrderPeriod, pk=pk)
    if request.method == "POST":
        form = OrderPeriodForm(request.POST, instance=order)
        startTime=form['start_time'].value()
        endTime=form['end_time'].value()
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
                return redirect('kilt:period_overview')

    form = OrderPeriodForm(instance=order)
    return render(request, "kiltshop/order_form.html", {'action':action,'form':form })

@login_required
def shop(request):
    user = request.user
    types = Product.type_choices
    now = datetime.datetime.now()
    active_order = OrderPeriod.objects.filter(end_time__gte=now).last()

    # Checks if there is an active timeframe
    active = False
    if active_order:
        active = True

    last_user_order = Order.objects.filter(user=user).last()
    if last_user_order:
        last_order_orderinfo = OrderPeriod.objects.filter(orders__id=last_user_order.pk).last()
    else:
        last_order_orderinfo = None
    # checks if the users last order is in the active timeframe.

    if last_order_orderinfo == active_order:
        current_user_order = last_user_order
    else:
        current_user_order = None

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
                if products is not None: # if you have selected products
                    if current_user_order != None: # if a user already has an order in this timeframe
                        for product in current_user_order.products.all():
                            if product.type == 'K':
                                has_kilt_id = product.pk
                                has_kilt = True
                            if product.type == 'S':
                                has_sporra = True
                                has_sporra_id = product.pk
                            if product.type == 'E':
                                for item in products:
                                    if str(item) == str(product.pk):
                                        m_qs = ProductInfo.objects.filter(order=current_user_order, product=item)
                                        m = m_qs.get()
                                        m.delete() # if you order the same product twice, we replace it with newest order

                        if has_kilt and new_kilt:
                            m_qs = ProductInfo.objects.filter(order=current_user_order, product=has_kilt_id)
                            m = m_qs.get()
                            m.delete() # removes ordered kilt if you order a new one

                        if has_sporra and new_sporra:
                            m_qs = ProductInfo.objects.filter(order=current_user_order, product=has_sporra_id)
                            m = m_qs.get()
                            m.delete() # removes ordered sporra if you order a new one

                        if comment:
                            current_user_order.comment = comment

                        for product in products:
                            number = int(request.POST.get('number-{id}'.format(id=product), 1))
                            if number > 0:
                                size = request.POST.get('size-{id}'.format(id=product), None)
                                item = Product.objects.get(pk=product)
                                productinfo = ProductInfo(order=current_user_order, product=item, size=size, number=number)
                                productinfo.save()
                            current_user_order.save()
                        current_user_order.save()
                        return redirect('kilt:info')
                    else:
                        order_list = Order.objects.create(user=user, period=active_order)
                        order_list.comment = comment
                        for product in products:
                            number = int(request.POST.get('number-{id}'.format(id=product), 1))
                            if number > 0:
                                size = request.POST.get('size-{id}'.format(id=product), None)
                                item = Product.objects.get(pk=product)
                                productinfo = ProductInfo(order=order_list, product=item, size=size, number=number)
                                productinfo.save()
                        order_list.save()
                        return redirect('kilt:info')

    return render(request, "kiltshop/shop.html",
                  {"products": Product.objects.all(),
                   'types':types,
                   'order': current_user_order,
                   'active': active
                   })
