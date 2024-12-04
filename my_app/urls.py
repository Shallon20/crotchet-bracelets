from django.urls import path
from . import views


urlpatterns = [
                  path('', views.home, name='home'),
                  path('about', views.about, name='about'),
                  path('product_list', views.product_list, name='products'),
                  path('category/<str:foo>', views.category, name='category'),
                  path('category_summary', views.category_summary, name='category_summary'),
                  # path('product_list/search', views.search_product, name='search_product'),
                  path('contact_us', views.contact_us, name='contact_us'),
                  path('thank_you', views.thank_you, name='thank_you'),
                  path('login', views.login_user, name='login'),
                  path('signup', views.signup_user, name='signup'),
                  path('logout', views.logout_user, name='logout'),
                  path('update_user', views.update_user, name='update_user'),
              ]
