import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from crud.work_center_crud import check_exists_work_center
from db.base import Base


@pytest.mark.asyncio
async def test_check_exists_work_center():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        # пустой список → []
        res = await check_exists_work_center([], session)
        assert res == []

        # фейковый батч
        class FakeBatch:
            work_center = "WC-1"

        fb = FakeBatch()
        out = await check_exists_work_center([fb], session)
        wc, batch = out[0]
        assert wc.name == "WC-1"
        assert batch is fb

    await engine.dispose()
