from django.db import models


class PaymentModel(models.Model):

    order_id = models.IntegerField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "payments"

    def __str__(self):
        return f"Payment {self.id} - Order {self.order_id}"
