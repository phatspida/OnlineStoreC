import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('cart:', cart)
    order = {'cost_total':0, 'item_count':0, 'shipping': False}
    orderitems = []
    
    for i in cart:
        try:
            order['item_count'] += cart[i]['quantity']
            product = Product.objects.get(id=i)
            order['cost_total'] += (product.price * cart[i]['quantity'])
            
            item = {
                'product' : {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL' : product.imageURL,
                },
                'quantity' : cart[i]['quantity'],
                'individual_item_total' : (cart[i]['quantity'] * product.price),
            }
            orderitems.append(item)

            if product.is_digital == False:
                order['shipping'] = True
        except:
            pass

    return {'order':order, 'orderitems':orderitems}


def cartData(request):
    current_user = request.user
    if current_user.is_authenticated:
        customer = current_user
        order, create = Order.objects.get_or_create(customer, completed=False)
        orderitems = order.orderitems_set.all()
        
    else:
        cookieitem = cookieCart(request)
        order = cookieitem['order']
        orderitems = cookieitem['orderitems']
    
    return {'order':order, 'orderitems':orderitems}