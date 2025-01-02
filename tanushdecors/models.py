import datetime
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('sofa', 'Sofa'),
        ('chair', 'Chair'),
        ('table', 'Table'),
    ]

    name = models.CharField(max_length=200, verbose_name="Product Name")  # Descriptive verbose name
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="Product Price"
    )
    pub_date = models.DateTimeField('Date Published', default=timezone.now)  # Defaults to now

    # Image Field
    image = models.ImageField(
        upload_to='images/', 
        default='images/default.jpg',  # Ensure a default image exists
        verbose_name="Product Image"
    )

    # Category Choices
    category = models.CharField(
        max_length=10, 
        choices=CATEGORY_CHOICES, 
        null=True,  # Allows NULL in the database
        blank=True,  # Field is optional in forms
        verbose_name="Product Category"
    )

    def was_published_recently(self):
        """Returns True if the product was published within the last day."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # Admin attributes for the `was_published_recently` method
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published Recently?'

    def __str__(self):
        """String representation of the Product model."""
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    

    # Order Model (Used to store user's orders)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

# OrderItem Model (Used to store products within a user's order)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order #{self.order.id}"

    # Method to calculate total price of this order item (quantity * price)
    def total_price(self):
        return self.quantity * self.product.price