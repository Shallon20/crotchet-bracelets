from django.db import models
from django.contrib.auth.models import User
from my_app.models import Product
from django.db.models.signals import post_save

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    shipping_full_name = models.CharField(max_length=100)
    shipping_email = models.EmailField(max_length=100)
    shipping_address1 = models.CharField(max_length=100)
    shipping_address2 = models.CharField(max_length=100, null=True, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=100, null=True, blank=True)
    shipping_country = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f"Shipping Address: - {str(self.id)}"

    # Create a shipping address by default when user signups
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

    # Automate the profile
post_save.connect(create_shipping, sender=User)


# Order Model
class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(decimal_places=2, max_digits=10)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f"Order - {str(self.id)}"
# Order items
class OrderItem(models.Model):
    # foreign keys
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"OrderItem - {str(self.id)}"