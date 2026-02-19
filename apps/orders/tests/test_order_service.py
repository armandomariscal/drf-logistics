import pytest

from apps.orders.application.services import OrderService
from apps.orders.domain.entities import Order
from apps.orders.domain.exceptions import (
    OrderAlreadyExists,
    OrderNotFound,
    InvalidOrderData
)


class FakeRepository:

    def __init__(self):
        self.orders = {}
        self.current_id = 1

    def save(self, order):

        if order.id is None:
            order.id = self.current_id
            self.current_id += 1

        self.orders[order.id] = order

        return order

    def get_by_id(self, order_id):

        return self.orders.get(order_id)
      
    def get_by_tracking_number(self, tracking_number):

        for order in self.orders.values():
            if order.tracking_number == tracking_number:
                return order

        return None

    def update(self, order):

        self.orders[order.id] = order

        return order

    def list(self):
        return list(self.orders.values())

def test_create_order_success():

    repo = FakeRepository()

    service = OrderService(repo)

    order = service.create_order(
        tracking_number="ABC123",
        customer_name="John",
        origin="NY",
        destination="LA",
    )

    assert order.id == 1
    assert order.status == "CREATED"


def test_assign_order_success():

    repo = FakeRepository()

    service = OrderService(repo)

    order = service.create_order(
        tracking_number="ABC123",
        customer_name="John",
        origin="NY",
        destination="LA",
    )

    assigned = service.assign_order(order.id)

    assert assigned.status == "ASSIGNED"


def test_cancel_order_success():

    repo = FakeRepository()

    service = OrderService(repo)

    order = service.create_order(
        tracking_number="ABC123",
        customer_name="John",
        origin="NY",
        destination="LA",
    )

    cancelled = service.cancel_order(order.id)

    assert cancelled.status == "CANCELLED"


def test_create_order_duplicate():

    repo = FakeRepository()
    service = OrderService(repo)

    service.create_order("ABC123", "John", "NY", "LA")

    with pytest.raises(OrderAlreadyExists):
        service.create_order("ABC123", "John", "NY", "LA")


def test_assign_order_not_found():

    repo = FakeRepository()
    service = OrderService(repo)

    with pytest.raises(OrderNotFound):
        service.assign_order(999)


def test_cancel_order_not_found():

    repo = FakeRepository()
    service = OrderService(repo)

    with pytest.raises(OrderNotFound):
        service.cancel_order(999)


def test_assign_order_invalid_status():

    repo = FakeRepository()
    service = OrderService(repo)

    order = service.create_order("ABC123", "John", "NY", "LA")

    service.assign_order(order.id)

    with pytest.raises(InvalidOrderData):
        service.assign_order(order.id)

def test_cancel_order_already_cancelled():

    repo = FakeRepository()
    service = OrderService(repo)

    order = service.create_order("ABC123", "John", "NY", "LA")

    service.cancel_order(order.id)

    with pytest.raises(InvalidOrderData):
        service.cancel_order(order.id)

def test_create_order_invalid_data():

    repo = FakeRepository()
    service = OrderService(repo)

    with pytest.raises(InvalidOrderData):
        service.create_order("", "John", "NY", "LA")
