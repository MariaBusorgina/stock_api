from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.schemas.order_item_schemas import OrderItemCreate, OrderItemSchema


class OrderBase(BaseModel):
    status: Optional[str] = "в процессе"


class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]


class OrderSchema(BaseModel):
    id: int
    created_at: datetime
    status: str
    order_items: List[OrderItemSchema]

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str
