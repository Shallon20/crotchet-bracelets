from django.contrib import admin

from my_app.models import Category, Product, CartOrder, CartItem, Customer

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
    search_fields = ['name', 'category']
    list_filter = ['category', 'price']
    list_per_page = 25

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_amount', 'shipping_address', 'status', 'created_at']
    search_fields = ['user', 'status', 'created_at']
    list_filter = ['user', 'status']
    list_per_page = 25

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'added_at']
    search_fields = ['user', 'product', 'added_at']
    list_filter = ['user', 'product', 'added_at']
    list_per_page = 25

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'address']
    search_fields = ['user', 'phone_number', 'address']
    list_filter = ['user', 'phone_number', 'address']
    list_per_page = 25


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Customer, CustomerAdmin)

# python3 manage.py createsuperuser

# admin2001 ---username
# shallonmaria2001@gmail.com ---email
# A@2001 ---password

#shallon
#Sha@2001

#maria
#maria01@gmail.com
#Maria@2001