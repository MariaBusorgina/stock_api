from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.repositories.order_repository import OrderRepository
from app.schemas.order_schema import OrderSchema, OrderCreate, OrderStatusUpdate

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@router.post("", response_model=OrderSchema, summary="Создать заказ",
             description="Создание нового заказа в базе данных.")
async def create_order(order_data: Annotated[OrderCreate, Depends()],
                       db: AsyncSession = Depends(get_db)):
    new_order = await OrderRepository.create_order(order_data, db)
    return new_order


@router.get("", response_model=List[OrderSchema], summary="Получить все заказы",
            description="Возвращает список всех заказов.")
async def get_orders(db: AsyncSession = Depends(get_db)):
    orders = await OrderRepository.get_all_orders(db)
    return orders


@router.get("/{id}", response_model=OrderSchema, summary="Получить заказ по ID",
            description="Возвращает заказ по указанному ID.")
async def get_order_by_id(id: int, db: AsyncSession = Depends(get_db)):
    order = await OrderRepository.get_order_by_id(id, db)
    return order


@router.patch("/{id}/status", response_model=OrderSchema, summary="Обновить статус заказа",
              description="Обновляет статус существующего заказа по его ID.")
async def update_order_status(id: int, status_update: Annotated[OrderStatusUpdate, Depends()],
                              db: AsyncSession = Depends(get_db)):
    order = await OrderRepository.update_order_status(id, status_update.status, db)
    return order
