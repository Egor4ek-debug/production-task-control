from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)

session = async_sessionmaker(bind=engine)


async def get_session():
    async with session() as s:
        yield s
