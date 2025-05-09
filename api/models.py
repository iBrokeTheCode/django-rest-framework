import uuid

from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    @property
    def in_stock(self) -> bool:
        return self.stock > 0

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = ('pending', 'Pending')
        CONFIRMED = ('confirmed', 'Confirmed')
        CANCELLED = ('cancelled', 'Cancelled')

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    products = models.ManyToManyField(
        Product, through='OrderItem', related_name='orders')

    def __str__(self) -> str:
        return f'Order: {self.order_id} by {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self) -> Decimal:
        return self.quantity * self.product.price

    def __str__(self) -> str:
        return f'{self.quantity} x {self.product.price} in Order {self.order.order_id}'
