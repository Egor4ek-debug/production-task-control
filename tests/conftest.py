import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from main import app
from models import Base
from core.db import get_session
from core.config import DATABASE_URL_TEST

# Создаём engine для тестов
engine_test = create_async_engine(DATABASE_URL_TEST, echo=False)
SessionTest = async_sessionmaker(bind=engine_test, expire_on_commit=False)


@pytest_asyncio.fixture()
async def db_session():
    """Изолированная БД-сессия для каждого теста."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionTest() as session:
        yield session


@pytest_asyncio.fixture()
async def client(db_session: AsyncSession):
    """HTTP-клиент с изолированной зависимостью"""
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()