from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.batch import router as batch_router
from api.product import router as product_router
from db.base import Base
from db.session import ENV, engine  # ENV и AsyncEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # — Startup —
    if ENV == "test":
        # для тестов: создаём схему в sqlite (in‑memory или test.db)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    yield  # теперь приложение принимает запросы

    # — Shutdown —
    if ENV == "test":
        # чистим схему по завершении тестов
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


# подключаем lifespan
app = FastAPI(title="Task Control API", lifespan=lifespan)

# ваши маршруты
app.include_router(batch_router)
app.include_router(product_router)
