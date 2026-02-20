from django.db import models
from apps.orders.domain.entities import OrderStatus


class OrderModel(models.Model):

    tracking_number = models.CharField(
        max_length=100,
        unique=True
    )

    customer_name = models.CharField(
        max_length=255
    )

    origin = models.CharField(
        max_length=255
    )

    destination = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.CHOICES,
        default=OrderStatus.CREATED
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "orders"

        indexes = [
            models.Index(fields=["tracking_number"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.tracking_number} - {self.status}"
