from django.db import models
from products.models import Product


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=255)

    def __str__(self):
        return self.product.name

    @property
    def total_price(self):
        return self.product.price * self.quantity