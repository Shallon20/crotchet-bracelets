from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from my_app.forms import ContactForm, LoginForm, SignupForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def products(request):
    return render(request, 'products.html')


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
    cart_items = [
        {'name': 'Crotchet Bag', 'price': 1500.00},
        {'name': 'Handmade Necklace', 'price': 800.00},
    ]
    return render(request, 'cart.html',{'cart_items': cart_items})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('cart')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
        else:
            form = SignupForm()
        return render(request, 'sign_up.html', {'form': form})
def log_out(request):
    logout(request)
    return redirect('login')

