from typing import Optional, List
from apps.orders.domain.entities import Order
from apps.orders.domain.repositories import OrderRepository
from apps.orders.infrastructure.models import OrderModel


class DjangoOrderRepository(OrderRepository):

    def save(self, order: Order) -> Order:

        if order.id:
            model = OrderModel.objects.get(id=order.id)
        else:
            model = OrderModel()

        model.tracking_number = order.tracking_number
        model.customer_name = order.customer_name
        model.origin = order.origin
        model.destination = order.destination
        model.status = order.status

        model.save()

        order.id = model.id

        return order


    def get_by_id(self, order_id: int) -> Optional[Order]:

        try:
            model = OrderModel.objects.get(id=order_id)

            return Order(
                id=model.id,
                tracking_number=model.tracking_number,
                customer_name=model.customer_name,
                origin=model.origin,
                destination=model.destination,
                status=model.status,
                created_at=model.created_at,
            )

        except OrderModel.DoesNotExist:
            return None


    def get_by_tracking_number(self, tracking_number: str) -> Optional[Order]:

        try:
            model = OrderModel.objects.get(tracking_number=tracking_number)

            return Order(
                id=model.id,
                tracking_number=model.tracking_number,
                customer_name=model.customer_name,
                origin=model.origin,
                destination=model.destination,
                status=model.status,
                created_at=model.created_at,
            )

        except OrderModel.DoesNotExist:
            return None


    def list(self) -> List[Order]:

        models = OrderModel.objects.all()

        return [
            Order(
                id=model.id,
                tracking_number=model.tracking_number,
                customer_name=model.customer_name,
                origin=model.origin,
                destination=model.destination,
                status=model.status,
                created_at=model.created_at,
            )
            for model in models
        ]
