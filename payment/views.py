from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from my_app.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Create your views here.
def payment_success(request):
    return render(request, 'payment/payment_success.html')
@login_required
def checkout(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # checkout as logged in
        # shipping user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html',
                      {'cart_products': cart_products, 'cart_total': totals, 'quantities': quantities,
                       'totals': totals, 'shipping_form': shipping_form})
    else:
        messages.error(request, "Please Login to place your order.")
        return render(request, 'login.html')

def billing_info(request):
    if request.POST:
        # get the cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants
        totals = cart.cart_total()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_info': request.POST, 'billing_form': billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',{'cart_products': cart_products, 'quantities': quantities, 'totals': totals,'shipping_info': request.POST, 'billing_form': billing_form})

        # shipping_form = request.POST
        # return render(request, 'payment/billing_info.html',{'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})
    else:
        messages.error(request, "Access Denied!!")
        return redirect('home')

def process_order(request):
    if request.POST:
        # get the cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get billing info from last page
        payment_form = PaymentForm(request.POST or None)
        # get shipping session data
        my_shipping = request.session.get('my_shipping')
        # Gather order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals
        # create an order
        if request.user.is_authenticated:
            user = request.user
            # create order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items
            # Get order id
            order_id = create_order.pk
            # get product info
            for product in cart_products:
                # get product id
                product_id = product.id
                # get product price
                if product.is_new:
                    price = product.price
                else:
                    price = product.price
                # get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id , user=user ,quantity=value, price=price)
                        create_order_item.save()
            # Delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # delete the key
                    del request.session[key]

            messages.success(request, 'Order Placed')
            return redirect('home')

        else:
            # not logged in
            # create order
            # create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address,
            #                      amount_paid=amount_paid)
            # create_order.save()
            #
            # messages.success(request, 'Order Placed')
            # return redirect('home')
            messages.success(request, 'Please Login to place your order.')
            return redirect('login')

    else:
        messages.error(request, 'Access Denied!!')
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    else:
        messages.error(request, "Access Denied!!")
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.error(request, "Access Denied!!")
        return redirect('home')


def orders(request, pk):
    # Get the orders
    order = Order.objects.get(id=pk)
    # get order items
    items = OrderItem.objects.filter(order=pk)
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'payment/orders.html', {'order': order, 'items': items})
    else:
        messages.error(request, "Access Denied!!")
        return redirect('home')


@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("M-Pesa Callback Received:", data)  # Logs to console
            # Optionally store or process transaction
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
        except Exception as e:
            print("Callback error:", e)
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Error"})
    return JsonResponse({"message": "Callback endpoint ready."})