import pytest
from unittest.mock import Mock

from apps.payments.application.services import PaymentService
from apps.payments.domain.entities import Payment, PaymentStatus
from apps.payments.infrastructure.repositories import DjangoPaymentRepository

from apps.orders.domain.entities import Order, OrderStatus
from apps.orders.infrastructure.repositories import DjangoOrderRepository

from apps.orders.domain.exceptions import OrderNotFound, InvalidOrderData


@pytest.fixture
def order_repo():
    return DjangoOrderRepository()


@pytest.fixture
def payment_repo():
    return DjangoPaymentRepository()


@pytest.fixture
def payment_service(payment_repo, order_repo):
    return PaymentService(payment_repo, order_repo)


@pytest.fixture
def mock_nats(monkeypatch):
    mock = Mock()
    monkeypatch.setattr("apps.payments.application.services.nats.publish", mock)
    return mock


@pytest.mark.django_db
def test_register_payment_success(payment_service, order_repo):

    order = Order(
        id=None,
        customer_name="John",
        address="Test street",
        status=OrderStatus.CREATED
    )

    order = order_repo.save(order)

    payment = payment_service.register_payment(order.id, 100.0)

    assert payment.id is not None
    assert payment.status == PaymentStatus.PENDING
    assert payment.amount == 100.0
    assert payment.order_id == order.id


@pytest.mark.django_db
def test_register_payment_order_not_found(payment_service):

    with pytest.raises(OrderNotFound):
        payment_service.register_payment(999, 100.0)


@pytest.mark.django_db
def test_confirm_payment_success(payment_service, order_repo, payment_repo, mock_nats):

    order = Order(
        id=None,
        customer_name="John",
        address="Test street",
        status=OrderStatus.CREATED
    )

    order = order_repo.save(order)

    payment = Payment(
        id=None,
        order_id=order.id,
        amount=100.0,
        status=PaymentStatus.PENDING
    )

    payment = payment_repo.save(payment)

    result = payment_service.confirm_payment(payment.id)

    updated_order = order_repo.get_by_id(order.id)

    assert result.status == PaymentStatus.CONFIRMED
    assert updated_order.status == OrderStatus.PAID

    mock_nats.assert_called_once_with(
        "OrderPaid",
        {
            "order_id": order.id,
            "amount": payment.amount
        }
    )


@pytest.mark.django_db
def test_confirm_payment_idempotent(payment_service, order_repo, payment_repo, mock_nats):

    order = Order(
        id=None,
        customer_name="John",
        address="Test street",
        status=OrderStatus.CREATED
    )

    order = order_repo.save(order)

    payment = Payment(
        id=None,
        order_id=order.id,
        amount=100.0,
        status=PaymentStatus.PENDING
    )

    payment = payment_repo.save(payment)

    payment_service.confirm_payment(payment.id)

    payment_service.confirm_payment(payment.id)

    updated_payment = payment_repo.get_by_id(payment.id)
    updated_order = order_repo.get_by_id(order.id)

    assert updated_payment.status == PaymentStatus.CONFIRMED
    assert updated_order.status == OrderStatus.PAID

    assert mock_nats.call_count == 1


@pytest.mark.django_db
def test_confirm_payment_not_found(payment_service):

    with pytest.raises(InvalidOrderData):
        payment_service.confirm_payment(999)


@pytest.mark.django_db
def test_confirm_payment_order_not_found(payment_service, payment_repo):

    payment = Payment(
        id=None,
        order_id=999,
        amount=100.0,
        status=PaymentStatus.PENDING
    )

    payment = payment_repo.save(payment)

    with pytest.raises(OrderNotFound):
        payment_service.confirm_payment(payment.id)
