from django.db import models
from account.models import User
from product.models import ProductVariant
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    is_paid = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f'{self.user} - {str(self.id)}'

    def total_payment(self):
        total = sum(item.get_payment_amount() for item in self.items.all())
        if self.discount != 0:
            discount = (self.discount / 100) * total
            return int(total - discount)
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_payment_amount(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
