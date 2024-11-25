from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from my_app.forms import ContactForm


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
def cart(request):
    return render(request, 'cart.html')


def login(request):
    return render(request, 'login.html')