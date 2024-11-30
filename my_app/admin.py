from django.contrib import admin

from my_app.models import Category, Product, CustomerOrder, Customer

# Register your models here.
admin.site.site_header = 'E&S Crotchet & Jewellery Administration'
admin.site.site_title = 'E&S Admin'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_filter = ['name']
    list_per_page = 25

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'price', 'is_sale', 'category', 'description']
    search_fields = ['name']
    list_filter = ['category', 'price']
    list_per_page = 25

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['user', 'total_amount', 'shipping_address', 'status', 'created_at']
#     search_fields = ['user', 'status', 'created_at']
#     list_filter = ['user', 'status']
#     list_per_page = 25
#
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ['user', 'product', 'quantity', 'added_at']
#     search_fields = ['user', 'product', 'added_at']
#     list_filter = ['user', 'product', 'added_at']
#     list_per_page = 25

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['first_name', 'last_name', 'email']
    list_per_page = 25

class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'status']
    search_fields = ['status', 'product']
    list_filter = ['status']
    list_per_page = 25

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CustomerOrder, CustomerOrderAdmin)
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