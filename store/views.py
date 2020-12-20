from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from .forms import UserRegisterForm
from django.contrib import messages


def homePage(request):
    return render(request, 'store/homepage.html')


def store(request):

    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        itemSize = data['itemSize']

        variation = Variation.objects.all()
        products = Product.objects.all()
        context = {'products': products,
                   'cartItems': cartItems, 'variation': variation}
        return render(request, 'store/store.html', context)
    else:
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        data = cartData(request)

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        itemSize = data['itemSize']

        context = {'items': items, 'order': order,
                   'cartItems': cartItems, 'itemSize': itemSize}
        return render(request, 'store/cart.html', context)
    else:
        return redirect('/register')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('store')
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html', {'form': form})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    variationSize = data['variationSize']
    print('Action:', action)
    print('Product:', productId)
    print('Variation:', variationSize)

    customer = request.user.customer
    variation = Variation.objects.get(id=variationSize)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product, variation=variation)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def checkout(request):
    if request.user.is_authenticated:
        data = cartData(request)

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        context = {'items': items, 'order': order, 'cartItems': cartItems}
        return render(request, 'store/checkout.html', context)
    else:
        return redirect('/register')


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            phone=data['shipping']['phone'],
        )

    return JsonResponse('Submitted..', safe=False)


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        itemSize = order.orderitem_set.all()
        cartItems = order.get_cart_items

        return {'cartItems': cartItems, 'order': order, 'items': items, 'itemSize': itemSize}
    else:
        pass
