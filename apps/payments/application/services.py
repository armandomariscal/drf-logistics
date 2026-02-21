from django.db import transaction

from apps.payments.domain.entities import Payment, PaymentStatus
from apps.payments.domain.repositories import PaymentRepository

from apps.orders.domain.entities import Order, OrderStatus
from apps.orders.domain.repositories import OrderRepository

from apps.orders.domain.exceptions import OrderNotFound, InvalidOrderData
from apps.messaging.nats import nats


class PaymentService:

    def __init__(self, payment_repo: PaymentRepository, order_repo: OrderRepository):
        self.payment_repo = payment_repo
        self.order_repo = order_repo


    def register_payment(self, order_id: int, amount: float) -> Payment:
        order = self.order_repo.get_by_id(order_id)

        if not order:
            raise OrderNotFound("Order not found")

        if order.status in [OrderStatus.CANCELLED, OrderStatus.IN_TRANSIT]:
            raise InvalidOrderData(
                "Cannot register payment for cancelled or in transit order"
            )

        payment = Payment(
            id=None,
            order_id=order_id,
            amount=amount,
            status=PaymentStatus.PENDING
        )

        return self.payment_repo.save(payment)


    @transaction.atomic
    def confirm_payment(self, payment_id: int) -> Payment:

        payment = self.payment_repo.get_by_id(payment_id)

        if not payment:
            raise InvalidOrderData("Payment not found")

        if payment.status == PaymentStatus.CONFIRMED:
            return payment

        payment.confirm()
        self.payment_repo.save(payment)

        order = self.order_repo.get_by_id(payment.order_id)

        if not order:
            raise OrderNotFound("Order not found")

        order_was_paid = order.status == OrderStatus.PAID

        if not order_was_paid:
            order.status = OrderStatus.PAID
            self.order_repo.save(order)

            nats.publish("OrderPaid", {
                "order_id": order.id,
                "amount": payment.amount
            })

        return payment