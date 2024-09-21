from pydantic import BaseModel, conint


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    # quantity должно быть больше 0
    quantity: conint(gt=0)


class OrderItemSchema(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True