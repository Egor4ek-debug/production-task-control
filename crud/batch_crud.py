from datetime import datetime, date
from typing import List, Optional, Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.work_center_crud import check_exists_work_center
from models.batch_model import Batch
from schemas.batch_schemas import BatchCreate, BatchResponse, BatchDetailResponse, BatchUpdate


def make_naive(dt: datetime) -> datetime:
    return dt.replace(tzinfo=None) if dt.tzinfo else dt


async def create_batches(batches: List[BatchCreate], session: AsyncSession) -> List[BatchResponse]:
    created_batches: List[Batch] = []
    worker_centers_and_batch = await check_exists_work_center(batches, session)
    for worker_center, batch in worker_centers_and_batch:
        batch_data = batch.model_dump(exclude="work_center")
        batch_data["shift_start_datetime"] = make_naive(batch.shift_start_datetime)
        batch_data["shift_end_datetime"] = make_naive(batch.shift_end_datetime)
        batch_data['work_center_id'] = worker_center.id

        batch_orm = Batch(**batch_data)
        session.add(batch_orm)
        await session.flush()
        created_batches.append(batch_orm)

    for batch in created_batches:
        await session.refresh(batch, attribute_names=["work_center"])
    return [BatchResponse.model_validate(batch) for batch in created_batches]


async def get_batch_by_id(batch_id: int, session: AsyncSession) -> BatchDetailResponse:
    result = await session.execute(
        select(Batch)
        .filter_by(id=batch_id)
        .options(
            selectinload(Batch.work_center)
            , selectinload(Batch.products),
        )
    )
    batch = result.scalar_one_or_none()

    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")

    return BatchDetailResponse.model_validate(batch)


async def update_batch_by_id(batch_id: int, batch_update: BatchUpdate, session: AsyncSession) -> Batch:
    result = await session.execute(
        select(Batch)
        .options(selectinload(Batch.work_center),
                 selectinload(Batch.products),
                 )
        .filter_by(id=batch_id)
    )
    batch = result.scalar_one_or_none()
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")

    update_data = batch_update.model_dump(exclude_none=True)

    for field, value in update_data.items():
        setattr(batch, field, value)
    if "is_closed" in update_data:
        if update_data["is_closed"]:
            batch.shift_end_datetime = datetime.now()
        else:
            batch.shift_end_datetime = None
    session.add(batch)
    await session.refresh(batch, attribute_names=["work_center", "products"])
    return batch


async def list_batches(
        session: AsyncSession,
        *,
        is_closed: Optional[bool] = None,
        batch_number: Optional[int] = None,
        batch_date_from: Optional[date] = None,
        batch_date_to: Optional[date] = None,
        limit: int = 50,
        offset: int = 0,
) -> Sequence[Batch]:
    q = select(Batch).options(
        selectinload(Batch.work_center)
    )

    if is_closed is not None:
        q = q.filter(Batch.is_closed == is_closed)
    if batch_number is not None:
        q = q.filter(Batch.batch_number == batch_number)
    if batch_date_from is not None:
        q = q.filter(Batch.batch_date >= batch_date_from)
    if batch_date_to is not None:
        q = q.filter(Batch.batch_date <= batch_date_to)

    q = q.order_by(Batch.batch_date.desc()).offset(offset).limit(limit)

    result = await session.scalars(q)
    return result.all()


async def get_batches_with_filters(
        session: AsyncSession,
        *,
        is_closed: Optional[bool],
        batch_number: Optional[int],
        batch_date: Optional[date],
        offset: int,
        limit: int,
) -> List[BatchResponse]:
    q = select(Batch).options(
        selectinload(Batch.work_center),
        selectinload(Batch.products),
    )

    if is_closed is not None:
        q = q.filter(Batch.is_closed == is_closed)
    if batch_number is not None:
        q = q.filter(Batch.batch_number == batch_number)
    if batch_date is not None:
        q = q.filter(Batch.batch_date == batch_date)

    q = q.offset(offset).limit(limit)

    result = await session.execute(q)
    batches = result.scalars().all()
    # Конвертация ORM → Pydantic
    return [BatchResponse.model_validate(b) for b in batches]
