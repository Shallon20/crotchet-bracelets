from django.contrib import admin
from django.contrib.auth.models import User
from my_app.models import Category, Product, CartOrder, Customer, CartItem, Profile

# Register your models here.
admin.site.site_header = 'E&S Crotchet & Jewellery Administration'
admin.site.site_title = 'E&S Admin'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_filter = ['name']
    list_per_page = 25

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'price', 'is_new', 'category', 'description']
    search_fields = ['name']
    list_filter = ['category', 'price']
    list_per_page = 25

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['user', 'total_amount', 'shipping_address', 'status', 'created_at']
#     search_fields = ['user', 'status', 'created_at']
#     list_filter = ['user', 'status']
#     list_per_page = 25

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'added_at']
    search_fields = ['product', 'added_at']
    list_filter = ['product', 'added_at']
    list_per_page = 25

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['first_name', 'last_name', 'email']
    list_per_page = 25

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'status']
    search_fields = ['status']
    list_filter = ['status']
    list_per_page = 25

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['phone', 'city', 'country']
    search_fields = ['phone', 'city', 'country']
    list_filter = ['city', 'country']
    list_per_page = 25

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Profile, ProfileAdmin)

# mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["Username", "first_name", "last_name", "Email"]
    list_display = ["first_name", "last_name"]
    inlines = [ProfileInline]

    # unregister the old way
admin.site.unregister(User)

# Re-register the new way
admin.site.register(User, UserAdmin)





# python3 manage.py createsuperuser

# admin2001 ---username
# shallonmaria2001@gmail.com ---email
# A@2001 ---password

#shallon
#Sha@2001

#Maria
#maria01@gmail.com
#Maria_2001