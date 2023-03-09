from django.shortcuts import render
from .models import *
from django.conf import settings
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData

def store(request):
    products = Product.objects.all()
    data = cartData(request)
    order = data['order']

    context = {
        'products': products,
        'title': 'Store',
        'order': order
        
    }
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    order = data['order']
    orderitems = data['orderitems']

    context = {
        'title': 'Cart',
        'order': order,
        'orderitems' : orderitems,
    } 
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    order = data['order']
    orderitems = data['orderitems']
    paystack_test_public_key = settings.PAYSTACK_TEST_PUBLIC_KEY

    context = {
        'title': 'Checkout',
        'order' : order,
        'orderitems': orderitems,
        'paystack_test_public_key': paystack_test_public_key
    }
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    product = Product.objects.get(id = productId)
    orderitems, created = OrderItems.objects.get_or_create(order=order, product=product)


    if action == 'add':
        orderitems.quantity = (orderitems.quantity + 1)
    elif action == 'remove':
        orderitems.quantity = (orderitems.quantity - 1)
    
    orderitems.save()

    if orderitems.quantity <= 0:
        orderitems.delete()
    
    return JsonResponse('Update Item is active. Data received', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    
    order = Order.objects.get_or_create(complete=False)
    order.complete = True
    order.save()

    return JsonResponse('Payment Submitted..', safe=False)