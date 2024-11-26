"""
URL configuration for crotchets_bracelets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from crotchets_bracelets import settings
from my_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product_list', views.product_list, name='products'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('thank_you', views.thank_you, name='thank_you'),
    path('cart', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('update_cart_quantity/<int:cart_item_id>/<str:action>', views.update_cart_quantity, name='update_cart_quantity'),
    path('login_user', views.login_user, name='login_user'),
    path('signup', views.signup, name='signup'),
    path('log_out', views.log_out, name='logout'),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

