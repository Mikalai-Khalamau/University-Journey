from dataclasses import dataclass
from uuid import UUID

@dataclass
class OrderItemInput:
    menu_item_id: UUID
    name: str
    price: float
    quantity: int = 1