from django.shortcuts import render, get_object_or_404
from .cart import Cart
from my_app.models import Product
from django.http import JsonResponse



# Create your views here.
def cart_summary(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants
    return render(request, 'cart_summary.html', {'cart_products': cart_products})
def cart_add(request):
    # get the cart
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # lookup product in database
        product = get_object_or_404(Product, id=product_id)
        #save to session
        cart.add(product=product, quantity=product_qty)
        # get cart quantity
        cart_quantity = cart.__len__()

        #return response
        # response = JsonResponse({'Product Name': 'product.name'})

        response = JsonResponse({'qty': cart_quantity})
        return response
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        # call delete function in cart
        cart.delete(product=product_id)
        response = JsonResponse({'qty': product_id})
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty': product_qty})
        return response
        #return redirect('cart_summary')