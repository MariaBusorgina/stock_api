from typing import Optional

from pydantic import BaseModel, confloat, conint


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int


class ProductCreate(ProductBase):
    price: confloat(gt=0)
    stock: conint(ge=0)


class ProductUpdate(ProductBase):
    pass


class ProductSchema(ProductBase):
    id: int

    class Config:
        from_attributes = True





