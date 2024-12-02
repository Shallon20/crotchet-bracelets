from django.urls import path
from . import views


urlpatterns = [
                  path('', views.home, name='home'),
                  path('about', views.about, name='about'),
                  # path('add/product', views.add_product, name='add_product'),
                  path('product_list', views.product_list, name='products'),
                  path('category/<str:foo>', views.category, name='category'),
                  path('product_list', views.product_detail, name='product_detail'),
                  # path('product_list/delete/<int:product_id>', views.delete_product, name='delete_product'),
                  # path('product_list/search', views.search_product, name='search_product'),
                  # path('product_list/update_product/<int:product_id>', views.update_product, name='update_product'),
                  path('contact_us', views.contact_us, name='contact_us'),
                  path('thank_you', views.thank_you, name='thank_you'),
                  # path('cart', views.cart, name='cart'),
                  # path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
                  # path('cart/update/<int:cart_item_id>/<str:action>', views.update_cart_quantity,
                  #      name='update_cart_quantity'),
                  # path('cart/remove/<int:cart_item_id>', views.remove_cart_item, name='remove_cart_quantity'),
                  path('login', views.login_user, name='login'),
                  path('signup', views.signup_user, name='signup'),
                  path('logout', views.logout_user, name='logout'),
              ]
