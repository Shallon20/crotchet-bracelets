from django.shortcuts import render, get_object_or_404
from .cart import Cart
from my_app.models import Product
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.
def cart_summary(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, 'cart_summary.html',
                  {'cart_products': cart_products, 'quantities': quantities, 'totals': totals})


def cart_add(request):
    # get the cart
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # lookup product in database
        product = get_object_or_404(Product, id=product_id)
        # save to session
        cart.add(product=product, quantity=product_qty)
        # get cart quantity
        cart_quantity = cart.__len__()

        # return response
        # response = JsonResponse({'Product Name': 'product.name'})

        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, 'Your product has been added to cart.')
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        # retrieve the product instance
        product = get_object_or_404(Product, id=product_id)
        # call delete function in cart
        cart.delete(product=product)
        response = JsonResponse({'qty': product_id})
        messages.success(request, 'Your product has been deleted from cart.')
        return response


def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('product_qty')

        # Check if both product_id and quantity are provided
        if not product_id or not quantity:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

        # Ensure that product_id and quantity are correct types
        product_id = str(product_id)
        quantity = int(quantity)

        # Update the cart with the new quantity
        cart.update(product_id, quantity)

        return JsonResponse({'status': 'success', 'message': 'Cart updated successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
