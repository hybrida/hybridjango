from django.shortcuts import render
from apps.merchandise.models import Product, Cart, Order, OrderElement
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic.edit import DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ProductForm

# Create your views here.
@login_required
def shop(request):
    products = Product.objects.all().order_by('category')

    return render(request, 'merchandise/shop.html', {'products': products})

@login_required
def product_page(request, pk):
    product = Product.objects.filter(pk=pk).first()
    i = 0
    for size in product.sizes.all():
        i += 1

    return render(request, 'merchandise/product_page.html', {'product': product, 'list_size': i})


@login_required
def AddItemToCart(request, pk):
    product = Product.objects.filter(pk=pk).first()
    elememt = OrderElement()
    elememt.product = product
    c = OrderElement.objects.all().order_by('id').last()
    if c:
        elememt.id = c.id + 1
        elememt.pk = c.pk + 1
    else:
        elememt.id = 1
        elememt.pk = 1

    if Cart.objects.all().filter(user=request.user):
        cart = Cart.objects.all().filter(user=request.user).first()
    else:
        c = Cart.objects.all().order_by('id').last()
        if c:
            cart = Cart()
            cart.id = c.id + 1
            cart.pk = c.pk + 1
            cart.user = request.user
        else:
            cart = Cart()
            cart.id = 1
            cart.pk = 1
            cart.user = request.user

    if request.POST:
        form_size = request.POST.get('size_form', '')
        number = request.POST.get('number', '')
        if request.user.is_authenticated:
            elememt.size = form_size
            elememt.number = number
            elememt.save()
            cart.save()
            cart.products.add(elememt)
            cart.save()
    return redirect('shop')


@login_required
def CartVeiw(request):
    user = request.user

    if Cart.objects.all().filter(user=user).first():
        cart = Cart.objects.all().filter(user=user).first()
    else:
        cart = Cart()
        c = Cart.objects.all().order_by('id').last()
        if c:
            cart = Cart()
            cart.id = c.id + 1
            cart.pk = c.pk + 1
            cart.user = request.user
        else:
            cart = Cart()
            cart.id = 1
            cart.pk = 1
            cart.user = request.user

    sum = 0
    for element in cart.products.all():
        sum += element.number * element.product.price

    return render(request, 'merchandise/cart.html', {'cart': cart, 'sum': sum})


@login_required
def OrderCart(request):
    cart = Cart.objects.all().filter(user=request.user).first()
    order = Order()
    c = Order.objects.all().order_by('id').last()
    if c:
        order.id = c.id + 1
        order.pk = c.pk + 1
    else:
        order.id = 1
        order.pk = 1

    sum = 0
    order.user = request.user
    cart.save()
    order.save()
    for e in cart.products.all():
        order.products.add(e)

    for element in cart.products.all():
        sum += element.number * element.product.price
    order.sum = sum

    order.timestamp = timezone.now()
    order.save()
    Cart.objects.all().filter(user=request.user).delete()
    return redirect('shop')


@permission_required(['merchandise.add_order'])
def OrderOverview(request):
    orders = Order.objects.all().order_by('pk').reverse()
    return render(request, 'merchandise/order_overview.html',{'orders':orders})



class DeleteOrderElement(DeleteView):
    model = OrderElement
    success_url = reverse_lazy('cartview')


@permission_required(['merchandise.add_order'])
def order_overview_product(request, pk):
    orders = Order.objects.all().order_by('pk').reverse()
    order = Order.objects.filter(pk=pk).first()
    elements = order.products.all()
    products = []
    i = 0
    for e in elements:
        products.append(e.product)


    return render(request, 'merchandise/order_overview_product.html', {'mainorder': order,'elements': elements,'orders': orders, 'products':products})


@permission_required(['merchandise.add_order'])
def order_status_change(request, pk):
    order = Order.objects.all().filter(pk=pk).first()
    if request.POST:
        pa = request.POST.get('paidForm')
        de = request.POST.get('deliveredForm')
        if request.user.is_authenticated:
            order.paid = pa
            order.delivered = de
            order.save()
    return redirect('order_overview')


class DeleteOrder(DeleteView):
    model = Order
    success_url = reverse_lazy('order_overview')


# def AddProduct(request):
#     form = ProductForm(request.POST)
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             application = form.save(commit=False)
#             application.save()
#             return redirect('shop')
#
#     return render(request, 'merchandise/product_form.html', {
#         'form': form,
#     })

class AddProduct(CreateView):
    model = Product
    fields = ['name', 'category', 'description', 'price', 'sizes', 'main_image', 'image1', 'image2', 'image3',
              'available']
