from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from deps.batch import get_batch_service
from schemas.batches import BatchRead, BatchCreate, BatchUpdate
from services.batches import BatchService

router = APIRouter(prefix="/batches")


@router.post("/", response_model=BatchRead)
async def create_batch(batch: BatchCreate, service: BatchService = Depends(get_batch_service)):
    return await service.create(batch)


@router.get("/{batch_id}", response_model=BatchRead)
async def get_batch_by_id(batch_id: int, service: BatchService = Depends(get_batch_service)):
    return await service.get_by_id(batch_id)


@router.patch("/{batch_id}", response_model=BatchRead)
async def update_batch(batch_id: int, update: BatchUpdate, service: BatchService = Depends(get_batch_service)):
    return await service.update(batch_id, update)


@router.get("/", response_model=List[BatchRead])
async def get_batch_filtered(is_closed: Optional[bool] = Query(None, description="Закрыта ли партия"),
                             number: Optional[int] = Query(None, description="Номер партии"),
                             date: Optional[date] = Query(None, description="Дата партии в формате YYYY-MM-DD"),
                             work_center_id: Optional[int] = Query(None, description="ID рабочего центра"),
                             shift: Optional[str] = Query(None, description="Смена: A, B, C и т.д."),
                             team: Optional[str] = Query(None, description="Название бригады"),
                             offset: int = Query(0, ge=0, description="Смещение для пагинации"),
                             limit: int = Query(100, ge=1, le=1000, description="Максимум записей за раз (1–1000)"),
                             service: BatchService = Depends(get_batch_service)) -> List[BatchRead]:
    return await service.get_filtered(is_closed=is_closed, batch_number=number, batch_date=date,
                                      work_center_id=work_center_id, shift=shift, team=team, offset=offset, limit=limit)
