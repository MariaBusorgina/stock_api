from fastapi import FastAPI

from app.api.order_routers import router as order_router
from app.api.product_routers import router as product_router
from app.database.database import init_db


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(product_router)
app.include_router(order_router)
