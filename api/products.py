from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from crud.products import ProductsRepository
from schemas.product_codes import ProductCodeBind, ProductAggregationResponse, ProductAggregationRequest

router = APIRouter(prefix="/products")


@router.post("/", response_model=List[ProductCodeBind])
async def bind_codes(product_data: List[ProductCodeBind], session: AsyncSession = Depends(get_session)) -> list[
    ProductCodeBind]:
    repo = ProductsRepository(session)

    result = await repo.create_products(product_data)

    return result


@router.post("/aggregate", response_model=ProductAggregationResponse)
async def create_products_with_aggregation(request: ProductAggregationRequest,
                                           session: AsyncSession = Depends(get_session)) -> ProductAggregationResponse:
    repo = ProductsRepository(session)
    result = await repo.aggregate_product(request.batch_id, request.code)

    return ProductAggregationResponse(code=result.code,aggregated_at=result.aggregated_at)
