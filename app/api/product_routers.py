from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductSchema

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.post("", response_model=ProductCreate, summary="Создать продукт",
             description="Создание нового продукта в базе данных.")
async def create_product(product: Annotated[ProductCreate, Depends()],
                         db: AsyncSession = Depends(get_db)):
    new_product = await ProductRepository.create_product(product.dict(), db)
    return new_product


@router.get("", response_model=List[ProductSchema], summary="Получить все продукты",
            description="Возвращает список всех продуктов из базы данных.")
async def get_products(db: AsyncSession = Depends(get_db)):
    products = await ProductRepository.get_all_products(db)
    return products


@router.get("/{id}", response_model=ProductSchema, summary="Получить продукт по ID",
            description="Возвращает информацию о продукте по указанному ID.")
async def get_product(id: int, db: AsyncSession = Depends(get_db)):
    product = await ProductRepository.get_product_by_id(id, db)
    return product


@router.put("/{id}", response_model=ProductSchema, summary="Обновить продукт по ID",
            description="Обновляет информацию о продукте по указанному ID.")
async def update_product(id: int,
                         product_update: Annotated[ProductCreate, Depends()],
                         db: AsyncSession = Depends(get_db)):
    updated_product = await ProductRepository.update_product(id, product_update, db)
    return updated_product


@router.delete("/{id}", status_code=204, summary="Удалить продукт по ID",
               description="Удаляет продукт по указанному ID.")
async def delete_product(id: int, db: AsyncSession = Depends(get_db)):
    await ProductRepository.delete_product(id, db)
    return None

