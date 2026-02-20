from abc import ABC, abstractmethod
from .entities import Payment


class PaymentRepository(ABC):
    
    @abstractmethod
    def save(self, payment: Payment) -> Payment:
        pass


    @abstractmethod
    def get_by_id(self, payment_id: int) -> Payment | None:
        pass


    @abstractmethod
    def list_by_order(self, order_id: int) -> list[Payment]:
        pass