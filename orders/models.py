from django.db import models
from products.models import Product
from customers.models import Customer


class Order(models.Model):

    ORDER_STATUS_CHOICES = [
        (0, 'Stage'),
        (1, 'Confirmed'),
        (2, 'Processed'),
        (3, 'Delivered'),
        (4, 'Rejected'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)

    order_status = models.PositiveIntegerField(
        choices=ORDER_STATUS_CHOICES,
        default=0
    )


    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    amount = models.PositiveBigIntegerField(default=0)  # store in paisa

    delete_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.owner.firstname if self.owner else 'Guest'}"

    @property
    def total_price(self):
        items = self.cart_items.filter(delete_status=False)
        return sum(item.total_price for item in items)


class OrderItem(models.Model):
    owner = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    delete_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    @property
    def total_price(self):
        return self.quantity * self.product.price
