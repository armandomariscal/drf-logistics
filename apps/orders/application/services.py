from apps.orders.domain.entities import Order, OrderStatus
from apps.orders.domain.repositories import OrderRepository
from apps.orders.domain.exceptions import (
    OrderAlreadyExists,
    OrderNotFound,
    InvalidOrderData
)
from apps.messaging.nats import nats


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

        # Business rules (Service Layer)

        if not tracking_number:
            raise InvalidOrderData("tracking_number is required")

        if not customer_name:
            raise InvalidOrderData("customer_name is required")

        if origin == destination:
            raise InvalidOrderData("origin and destination cannot be the same")

        existing = self.repository.get_by_tracking_number(tracking_number)

        if existing:
            raise OrderAlreadyExists(
                "Order with this tracking number already exists"
        )

        order = Order(
            id=None,
            tracking_number=tracking_number,
            customer_name=customer_name,
            origin=origin,
            destination=destination,
            status=OrderStatus.CREATED,
        )

        saved_order = self.repository.save(order)
        
        nats.publish("OrderCreated", {"order_id": saved_order.id})
        
        return saved_order


    def get_order(self, order_id: int):

        order = self.repository.get_by_id(order_id)

        if not order:
            raise OrderNotFound("Order not found")

        return order


    def list_orders(self):

        return self.repository.list()


    def assign_order(self, order_id: int, driver_id: int) -> Order:

        order = self.repository.get_by_id(order_id)

        if not order:
            raise OrderNotFound("Order not found")

        if order.status != OrderStatus.CREATED:
            raise InvalidOrderData("Only CREATED orders can be assigned")

        order.driver_id = driver_id
        order.status = "ASSIGNED"

        return self.repository.save(order)
    

    def cancel_order(self, order_id: int) -> Order:

        order = self.repository.get_by_id(order_id)

        if not order:
            raise OrderNotFound("Order not found")

        if order.status == "CANCELLED":
            raise InvalidOrderData("Order already cancelled")

        if order.status == "IN_TRANSIT":
            raise InvalidOrderData("Cannot cancel in transit order")

        order.status = "CANCELLED"

        return self.repository.save(order)