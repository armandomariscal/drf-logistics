from enum import Enum
from apps.payments.domain.exceptions import PaymentAlreadyConfirmed


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"


class Payment:

    def __init__(
        self,
        id: int | None,
        order_id: int,
        amount: float,
        status: PaymentStatus,
    ):
        self.id = id
        self.order_id = order_id
        self.amount = amount
        self.status = status


    def confirm(self):
        if self.status == PaymentStatus.CONFIRMED:
            raise PaymentAlreadyConfirmed("Payment already confirmed")

        self.status = PaymentStatus.CONFIRMED
