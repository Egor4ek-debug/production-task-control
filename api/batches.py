from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from crud.batches import BatchRepository
from exceptions.http_exceptions import NotFoundException
from schemas.batches import BatchRead, BatchCreate, BatchUpdate

router = APIRouter(prefix="/batches")


@router.post("/", response_model=BatchRead)
async def create_batch(batch: BatchCreate, session: AsyncSession = Depends(get_session)) -> BatchRead:
    repo = BatchRepository(session)
    return await repo.create(batch)


@router.get("/{batch_id}", response_model=BatchRead)
async def get_batch_by_id(batch_id: int, session: AsyncSession = Depends(get_session)) -> BatchRead:
    repo = BatchRepository(session)
    result = await repo.get_by_id(batch_id)
    if result is None:
        raise NotFoundException(detail=f"Batch not found for id={batch_id}")
    return result


@router.patch("/{batch_id}", response_model=BatchRead)
async def update_batch(batch_id: int, batch: BatchUpdate, session: AsyncSession = Depends(get_session)) -> BatchRead:
    repo = BatchRepository(session)
    result = await repo.update(batch_id, batch)
    return result


@router.get("/", response_model=List[BatchRead])
async def get_batch_filtered(is_closed: Optional[bool] = Query(None), batch_number: Optional[int] = Query(None),
                             batch_date: Optional[date] = Query(None), work_center_id: Optional[int] = Query(None),
                             shift: Optional[str] = Query(None), team: Optional[str] = Query(None),
                             offset: int = Query(0, ge=0), limit: int = Query(100, le=1000),
                             session: AsyncSession = Depends(get_session)) -> List[BatchRead]:
    repo = BatchRepository(session)
    result = await repo.get_filtered(is_closed, batch_number, batch_date, work_center_id, shift, team, offset, limit)
    return result
