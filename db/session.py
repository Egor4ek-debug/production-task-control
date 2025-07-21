import os

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import DATABASE_URL as prod_url_db

# режим по‑умолчанию — «прод»
ENV = os.getenv('ENV', 'prod')

# Для тестов можно передавать свой DB_URL_TESTS, или по‑умолчанию sqlite файл
if ENV == 'test':
    DATABASE_URL = os.getenv('DB_URL_TESTS', 'sqlite+aiosqlite:///./test.db')
else:
    DATABASE_URL = prod_url_db

# создаём AsyncEngine; у него автоматически появится .sync_engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

# фабрика для сессий
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Депенденси для FastAPI
async def get_async_session():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
