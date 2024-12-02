import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, default="", blank=True, null=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/images/')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_new = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category']
        db_table = 'product'
        verbose_name_plural = 'Products'


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def total_price(self):
        return self.product.price * self.quantity


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'customer'


class CartOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default="", blank=True, null=True)
    phone_number = models.CharField(max_length=20, default="", blank=True, null=True)
    date = models.DateTimeField(default=datetime.datetime.now)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name}(Customer: {self.customer.first_name})"

    class Meta:
        db_table = 'cart_order'
        verbose_name_plural = 'cart_orders'
