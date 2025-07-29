import datetime
from datetime import date
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from exceptions.http_exceptions import NotFoundException
from interfaces.repositories import IBatchRepository
from models import Batch
from schemas.batches import BatchCreate, BatchUpdate


class BatchRepository(IBatchRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, batch_data: BatchCreate):

        batch_orm = Batch(**batch_data.model_dump())

        self.session.add(batch_orm)

        await self.session.commit()
        await self.session.refresh(batch_orm)
        return batch_orm

    async def get_by_id(self, batch_id: int) -> Batch | None:

        stmt = (select(Batch)
                .options(selectinload(Batch.product_codes))
                .filter_by(id=batch_id))
        result = await self.session.execute(stmt)
        batch = result.scalars().first()
        return batch

    async def update(self, batch_id: int, update_data: BatchUpdate) -> Batch:
        result = await self.get_by_id(batch_id)
        if result is None:
            raise NotFoundException(detail=f"Batch not found for id={batch_id}")
        data = update_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(result, key, value)

        if "is_closed" in data:
            if data["is_closed"]:
                result.closed_at = datetime.datetime.now()
            else:
                setattr(result, "is_closed", None)

        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def get_filtered(self, is_closed: Optional[bool] = None, batch_number: Optional[int] = None,
                           batch_date: Optional[date] = None,
                           work_center_id: Optional[int] = None, shift: Optional[str] = None,
                           team: Optional[str] = None, offset: int = 0,
                           limit: int = 100) -> list[Batch]:
        stmt = (select(Batch)
                .options(selectinload(Batch.product_codes)))

        if is_closed is not None:
            stmt = stmt.filter_by(is_closed=is_closed)
        if batch_number is not None:
            stmt = stmt.filter_by(batch_number=batch_number)
        if batch_date is not None:
            stmt = stmt.filter_by(batch_date=batch_date)
        if work_center_id is not None:
            stmt = stmt.filter_by(work_center_id=work_center_id)
        if shift is not None:
            stmt = stmt.filter_by(shift=shift)
        if team is not None:
            stmt = stmt.filter_by(team=team)

        stmt = stmt.offset(offset).limit(limit)

        result = await self.session.execute(stmt)

        batches = result.scalars().all()

        return batches

