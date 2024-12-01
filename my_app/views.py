from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from my_app.forms import ContactForm, LoginForm, SignupForm, ProductForm
from my_app.models import Product, Category, CartOrder, CartItem


# Create your views here.
def home(request):
    products = Product.objects.all()
    # latest_products = Product.objects.order_by('-created_at')[:6]  # [:6] limits the query to fetch only the top 6 products
    return render(request, 'home.html', {"products": products})

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

@login_required
def update_product(request, product_id):
    return None

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

def thank_you(request):
    return render(request, 'thank_you.html')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html',{
        'cart_items': cart_items,
        'total_price': total_price
    })
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1},
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to your cart!")
    return redirect('cart')
@login_required()
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, "Your cart is empty! Add items before placing an order.")
        return redirect('cart')
    total_amount = sum(item.total_price() for item in cart_items)

    order = CartOrder.objects.create(
        user=request.user,
        total_amount=total_amount,
        shipping_address=request.POST.get('shipping_address', 'Default Address'),

    )
    for item in cart_items:
        item.delete()

    messages.success(request, "Your order has been placed successfully!.")
    return redirect('home')
@login_required()
def update_cart_quantity(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        cart_item.delete()
        return JsonResponse({
        'quantity': 0,
        'total_price':  0,
        'cart_total': sum(item.total_price() for item in cart_item.objects.filter(user=request.user)),
        })
    cart_item.save()
    return JsonResponse({
        'quantity': cart_item.quantity,
        'total_price': cart_item.total_price(),
        'cart_total': sum(item.total_price() for item in CartItem.objects.filter(user=request.user)),
    })

@login_required()
def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Your cart item has been removed successfully!")
    return JsonResponse({'status': 'success'})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are now logged in!")
                return redirect('home')

            else:
                messages.error(request, 'There was an error, Please try again.')
                return redirect('login')
    else:
        return render(request, 'login.html', {})

def signup_user(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login_user')
        else:
            messages.error(request, 'Whoops! There was an error, Please try again.')
            return redirect('signup_user')
    else:
        return render(request, 'sign_up.html', {'form': form})
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
@permission_required("my_app.delete_product", raise_exception=True)
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.info(request, f"Customer {product.name} was deleted!!")
    return redirect('products')

@login_required
@permission_required("my_app.add_product", raise_exception=True)
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product {form.cleaned_data['name']} was added!")
            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'product_add_form.html', {"form": form})

@login_required
@permission_required("my_app.change_product", raise_exception=True)
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product {form.cleaned_data['name']} was updated!")
            return redirect('products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_update_form.html', {"form": form})


@login_required
@permission_required("my_app.view_product", raise_exception=True)
def search_product(request):
    if request.method == "POST":
        searched = request.POST['searched']
        products = Product.objects.filter(name__contains=searched)
        return render(request, "search.html", {'searched': searched, 'products': products})
    else:
        return render(request, "search.html", {})

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


