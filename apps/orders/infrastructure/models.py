from django.db import models


class OrderModel(models.Model):

    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        ASSIGNED = "ASSIGNED", "Assigned"
        IN_TRANSIT = "IN_TRANSIT", "In Transit"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

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
        choices=Status.choices,
        default=Status.CREATED
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
