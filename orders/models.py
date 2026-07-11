from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Out For Delivery", "Out For Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    # ==========================
    # User & Product
    # ==========================

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # ==========================
    # Order Status
    # ==========================

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    cancel_reason = models.TextField(
        blank=True,
        default=""
    )

    # ==========================
    # Customer Details
    # ==========================

    full_name = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        default="India"
    )

    # ==========================
    # Invoice
    # ==========================

    invoice_no = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # ==========================
    # Save Invoice Number
    # ==========================

    def save(self, *args, **kwargs):

        creating = self.pk is None

        super().save(*args, **kwargs)

        if creating and not self.invoice_no:

            self.invoice_no = f"INV{self.id:05d}"

            super().save(update_fields=["invoice_no"])

    # ==========================
    # String
    # ==========================

    def __str__(self):

        if self.invoice_no:
            return f"{self.invoice_no} - {self.user.username}"

        return f"Order #{self.id} - {self.user.username}"