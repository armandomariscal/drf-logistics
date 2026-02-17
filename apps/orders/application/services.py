from apps.orders.domain.entities import Order
from apps.orders.domain.repositories import OrderRepository


class OrderService:

    def __init__(self, repository: OrderRepository):
        self.repository = repository


    def create_order(
        self,
        tracking_number: str,
        customer_name: str,
        origin: str,
        destination: str,
    ) -> Order:

        existing = self.repository.get_by_tracking_number(tracking_number)

        if existing:
            raise Exception("Order with this tracking number already exists")

        order = Order(
            id=None,
            tracking_number=tracking_number,
            customer_name=customer_name,
            origin=origin,
            destination=destination,
            status="CREATED",
        )

        return self.repository.save(order)


    def get_order(self, order_id: int):

        order = self.repository.get_by_id(order_id)

        if not order:
            raise Exception("Order not found")

        return order


    def list_orders(self):

        return self.repository.list()
