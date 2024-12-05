from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from my_app.forms import ContactForm, LoginForm, SignupForm, UpdateUserForm, ChangePasswordForm
from my_app.models import Product, Category, CartOrder, CartItem


# Create your views here.
def home(request):
    products = Product.objects.all()
    latest_products = Product.objects.filter(is_new=True)[:6]  # [:6] limits the query to fetch only the top 6 products
    return render(request, 'home.html', {"products": products, "latest_products": latest_products})


def product_list(request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category_name=category)
    else:
        products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'products.html', {"products": products, "categories": categories})


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


# @login_required
# @permission_required("my_app.view_product", raise_exception=True)
def search_product(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '').strip()
        if searched:
            products = Product.objects.filter(name__icontains=searched)
            return render(request, "search.html", {'searched': searched, 'products': products})
        return render(request, "search.html", {'error': 'Please enter a search term.'})
    return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password updated successfully!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return render(request, 'update_password.html', {'form': form})

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.error(request, 'You are not logged in.')
        return redirect('login')