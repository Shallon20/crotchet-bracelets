from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


import my_app
from crotchets_bracelets import settings
from cart import views

urlpatterns = [
                path('', views.cart_summary, name='cart_summary'),
                path('add', views.cart_add, name='cart_add'),
                path('delete', views.cart_delete, name='cart_delete'),
                path('update', views.cart_update, name='cart_update'),
              ]