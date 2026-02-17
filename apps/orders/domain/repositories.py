from abc import ABC, abstractmethod
from typing import Optional, List
from apps.orders.domain.entities import Order


class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def get_by_tracking_number(self, tracking_number: str) -> Optional[Order]:
        pass

    @abstractmethod
    def list(self) -> List[Order]:
        pass
