from django.contrib.auth.decorators import login_required
from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect

from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress


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

        if request.user.is_authenticated:
            return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': request.POST})
        else:
            return render(request, 'payment/billing_info.html',{'cart_products': cart_products, 'quantities': quantities, 'totals': totals,'shipping_form': request.POST})

        shipping_form = request.POST
        return render(request, 'payment/billing_info.html',{'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})
    else:
        # messages.error(request, "Access Denied!!")
        return redirect('home')