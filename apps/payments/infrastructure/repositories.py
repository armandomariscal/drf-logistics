from apps.payments.domain.entities import Payment, PaymentStatus
from apps.payments.domain.repositories import PaymentRepository

from apps.payments.infrastructure.models import PaymentModel


class DjangoPaymentRepository(PaymentRepository):

    def save(self, payment: Payment) -> Payment:

        if payment.id is None:

            model = PaymentModel.objects.create(
                order_id=payment.order_id,
                amount=payment.amount,
                status=payment.status.value,
            )

        else:

            model = PaymentModel.objects.get(id=payment.id)

            model.order_id = payment.order_id
            model.amount = payment.amount
            model.status = payment.status.value

            model.save()

        return self._to_entity(model)


    def get_by_id(self, payment_id: int) -> Payment | None:

        try:
            model = PaymentModel.objects.get(id=payment_id)
            return self._to_entity(model)

        except PaymentModel.DoesNotExist:
            return None


    def list_by_order(self, order_id: int) -> list[Payment]:

        models = PaymentModel.objects.filter(order_id=order_id)

        return [self._to_entity(model) for model in models]


    def _to_entity(self, model: PaymentModel) -> Payment:

        return Payment(
            id=model.id,
            order_id=model.order_id,
            amount=float(model.amount),
            status=PaymentStatus(model.status),
        )
