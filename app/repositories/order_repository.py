from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.models import Order, Product, OrderItem
from app.schemas.order_schema import OrderCreate


class OrderRepository:
    """Репозиторий для управления заказами в базе данных."""
    @staticmethod
    async def create_order(order_data: OrderCreate, db: AsyncSession) -> Order:
        """Создать заказ."""
        async with db.begin():
            # Проверка наличия всех продуктов
            await OrderRepository._check_product_availability(order_data, db)

            # Создание нового заказа
            new_order = Order(status=order_data.status)
            db.add(new_order)
            await db.flush()

            # Добавление элементов заказа и обновление склада
            await OrderRepository._add_order_items_and_update_stock(order_data, new_order, db)

        await db.commit()
        await db.refresh(new_order)

        # Возвращаем заказ с загруженными элементами
        order = await OrderRepository.get_order_by_id(new_order.id, db)
        return order

    @staticmethod
    async def _check_product_availability(order_data: OrderCreate, db: AsyncSession):
        """Проверить наличие продуктов и достаточность запасов."""
        for item in order_data.order_items:
            product = await db.get(Product, item.product_id)
            if product is None:
                raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
            if product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for product id {item.product_id}")

    @staticmethod
    async def _add_order_items_and_update_stock(order_data: OrderCreate, order: Order, db: AsyncSession):
        """Добавить элементы заказа, обновить остатки склада."""
        for item in order_data.order_items:
            new_order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.add(new_order_item)

            product = await db.get(Product, item.product_id)
            if product:
                product.stock -= item.quantity

    @staticmethod
    async def get_all_orders(db: AsyncSession) -> List[Order]:
        """Получить все заказы."""
        query = select(Order).options(joinedload(Order.order_items))
        result = await db.execute(query)
        orders = result.scalars().unique().all()
        return orders

    @staticmethod
    async def get_order_by_id(id: int, db: AsyncSession) -> Order:
        """Получить заказ по его ID."""
        query = select(Order).options(joinedload(Order.order_items)).filter(Order.id == id)
        result = await db.execute(query)
        order = result.unique().scalar_one_or_none()

        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    @staticmethod
    async def update_order_status(id: int, status: str, db: AsyncSession) -> Order:
        """Обновить статус заказа по его ID."""
        order = await OrderRepository.get_order_by_id(id, db)
        order.status = status
        await db.commit()
        await db.refresh(order)
        return order