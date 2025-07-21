from datetime import date
from typing import List, Optional

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from crud.batch_crud import create_batches, get_batch_by_id, update_batch_by_id, get_batches_with_filters
from db.session import get_async_session
from schemas.batch_schemas import BatchCreate, BatchResponse, BatchDetailResponse, BatchUpdate

router = APIRouter()


@router.post("/batches", response_model=List[BatchResponse])
async def create_batches_endpoint(batches: List[BatchCreate], session: AsyncSession = Depends(get_async_session)) -> \
        List[BatchResponse]:
    result = await create_batches(batches, session)

    return result


@router.get("/batches/{batch_id}", response_model=BatchDetailResponse)
async def get_batch_and_products_by_id(batch_id: int,
                                       session: AsyncSession = Depends(get_async_session)) -> BatchDetailResponse:
    return await get_batch_by_id(batch_id, session)


@router.patch("/batches/{batch_id}", response_model=BatchResponse)
async def patch_batch_by_id(batch_id: int, patch: BatchUpdate,
                            session: AsyncSession = Depends(get_async_session)) -> BatchResponse:
    batch = await update_batch_by_id(batch_id, patch, session)
    return BatchResponse.model_validate(batch)


@router.get(
    "/batches",
    response_model=List[BatchResponse],
    summary="Список сменных заданий с фильтрами и пагинацией"
)
async def list_batches(
        is_closed: Optional[bool] = Query(None),
        batch_number: Optional[int] = Query(None),
        batch_date: Optional[date] = Query(None),
        offset: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        session: AsyncSession = Depends(get_async_session),
) -> List[BatchResponse]:
    return await get_batches_with_filters(
        session,
        is_closed=is_closed,
        batch_number=batch_number,
        batch_date=batch_date,
        offset=offset,
        limit=limit,
    )
