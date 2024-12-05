from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from my_app.forms import ContactForm, LoginForm, SignupForm, UpdateUserForm
from my_app.models import Product, Category, CartOrder, CartItem


# Create your views here.
def home(request):
    products = Product.objects.all()
    latest_products = Product.objects.filter(is_new=True)[:6]  # [:6] limits the query to fetch only the top 6 products
    return render(request, 'home.html', {"products": products, "latest_products": latest_products})


def about(request):
    return render(request, 'about.html')


def product_list(request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category_name=category)
    else:
        products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'products.html', {"products": products, "categories": categories})


def product_detail(request, product_id):
    products = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'products': products})


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            print(f"Message from {name} ({email}): {message}")
            return HttpResponseRedirect('/thank_you')

    else:
        form = ContactForm()

    return render(request, 'contact_us.html', {'form': form})


def category(request, foo):
    # Replaces hyphens with spaces
    foo = foo.replace('-', '')
    # Grab category from url
    try:
        # look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, "category.html", {'category': category, 'products': products})
    except:
        messages.error(request, 'Please enter a valid category.')
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})


@login_required
def update_user(request):
    current_user = request.user  # Access the currently logged-in user
    user_form = UpdateUserForm(request.POST or None, instance=current_user)

    if request.method == 'POST':
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('home')
        else:
            messages.error(request, "There was an error updating your profile.")

    return render(request, 'update_user.html', {'user_form': user_form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "You are now logged in!")
                return redirect('home')

            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill the form correctly')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Welcome!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()

    return render(request, 'sign_up.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def thank_you(request):
    return render(request, 'thank_you.html')


@login_required
def update_product(request, product_id):
    return None


# @login_required
# def cart(request):
#     cart_items = CartItem.objects.filter(user=request.user)
#     total_price = sum(item.total_price() for item in cart_items)
#     return render(request, 'cart.html',{
#         'cart_items': cart_items,
#         'total_price': total_price
#     })
# @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart_item, created = CartItem.objects.get_or_create(
#         user=request.user,
#         product=product,
#         defaults={'quantity': 1},
#     )
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     messages.success(request, f"{product.name} added to your cart!")
#     return redirect('cart')
# @login_required()
# def place_order(request):
#     cart_items = CartItem.objects.filter(user=request.user)
#     if not cart_items:
#         messages.error(request, "Your cart is empty! Add items before placing an order.")
#         return redirect('cart')
#     total_amount = sum(item.total_price() for item in cart_items)
#
#     order = CartOrder.objects.create(
#         user=request.user,
#         total_amount=total_amount,
#         shipping_address=request.POST.get('shipping_address', 'Default Address'),
#
#     )
#     for item in cart_items:
#         item.delete()
#
#     messages.success(request, "Your order has been placed successfully!.")
#     return redirect('home')
# @login_required()
# def update_cart_quantity(request, cart_item_id, action):
#     cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
#
#     if action == 'increase':
#         cart_item.quantity += 1
#     elif action == 'decrease' and cart_item.quantity > 1:
#         cart_item.quantity -= 1
#     else:
#         cart_item.delete()
#         return JsonResponse({
#         'quantity': 0,
#         'total_price':  0,
#         'cart_total': sum(item.total_price() for item in cart_item.objects.filter(user=request.user)),
#         })
#     cart_item.save()
#     return JsonResponse({
#         'quantity': cart_item.quantity,
#         'total_price': cart_item.total_price(),
#         'cart_total': sum(item.total_price() for item in CartItem.objects.filter(user=request.user)),
#     })

# @login_required()
# def remove_cart_item(request, cart_item_id):
#     cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
#     cart_item.delete()
#     messages.success(request, "Your cart item has been removed successfully!")
#     return JsonResponse({'status': 'success'})


# @login_required
# @permission_required("my_app.delete_product", raise_exception=True)
# def delete_product(request, product_id):
#     product = Product.objects.get(id=product_id)
#     product.delete()
#     messages.info(request, f"Customer {product.name} was deleted!!")
#     return redirect('products')
#
# @login_required
# @permission_required("my_app.add_product", raise_exception=True)
# def add_product(request):
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Product {form.cleaned_data['name']} was added!")
#             return redirect('products')
#     else:
#         form = ProductForm()
#     return render(request, 'product_add_form.html', {"form": form})
#
# @login_required
# @permission_required("my_app.change_product", raise_exception=True)
# def update_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Product {form.cleaned_data['name']} was updated!")
#             return redirect('products')
#     else:
#         form = ProductForm(instance=product)
#     return render(request, 'product_update_form.html', {"form": form})

#
# @login_required
# @permission_required("my_app.view_product", raise_exception=True)
def search_product(request):
    if request.method == "POST":
        searched = request.POST['searched']
        products = Product.objects.filter(name__contains=searched)
        return render(request, "search.html", {'searched': searched, 'products': products})
    else:
        return render(request, "search.html", {})
