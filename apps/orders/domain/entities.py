from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Order:
    id: Optional[int]
    tracking_number: str
    customer_name: str
    origin: str
    destination: str
    status: str
    created_at: Optional[datetime] = None


class OrderStatus:
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    PAID = "PAID"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

    CHOICES = [
        (CREATED, "Created"),
        (ASSIGNED, "Assigned"),
        (PAID, "Paid"),
        (IN_TRANSIT, "In Transit"),
        (DELIVERED, "Delivered"),
        (CANCELLED, "Cancelled"),
    ]
