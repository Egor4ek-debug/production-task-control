# tests/conftest.py
import os
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from db.base import Base

# до импорта приложения
os.environ["ENV"] = "test"

# чисто синхронный движок на файл test.db
sync_engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False},
    future=True,
)


@pytest.fixture(autouse=True)
def setup_test_db():
    # перед каждым тестом честно чистим и создаём схему
    Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)
    yield


from main import app


@pytest.fixture
def client():
    return TestClient(app)
