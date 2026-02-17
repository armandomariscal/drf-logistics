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
