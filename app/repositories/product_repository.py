from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.models import Product
from app.schemas.product_schema import ProductCreate


class ProductRepository:
    """Репозиторий для управления товарами в базе данных."""
    @staticmethod
    async def create_product(product_data: dict, db: AsyncSession) -> Product:
        """Создать новый товар."""
        new_product = Product(**product_data)
        db.add(new_product)
        try:
            await db.commit()
            await db.refresh(new_product)
            return new_product
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this name already exists"
            )

    @staticmethod
    async def get_all_products(db: AsyncSession) -> List[Product]:
        """Получить список всех товаров."""
        query = select(Product)
        result = await db.execute(query)
        products = result.scalars().all()
        return products

    @staticmethod
    async def get_product_by_id(id: int, db: AsyncSession) -> Product:
        """Получить продукт по его ID."""
        query = select(Product).filter(Product.id == id)
        result = await db.execute(query)
        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    @staticmethod
    async def update_product(id: int, product_update: ProductCreate, db: AsyncSession) -> Product:
        """Обновить продукт по его ID."""
        product = await ProductRepository.get_product_by_id(id, db)
        for key, value in product_update.dict().items():
            setattr(product, key, value)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def delete_product(id: int, db: AsyncSession):
        """Удалить продукт по его ID."""
        product = await ProductRepository.get_product_by_id(id, db)
        await db.delete(product)
        await db.commit()
