from typing import List

from fastapi import APIRouter, Depends

from deps.products import get_product_service
from schemas.product_codes import ProductCodeBind, ProductAggregationResponse, ProductAggregationRequest
from services.products import ProductsService

router = APIRouter(prefix="/products")


@router.post("/", response_model=List[ProductCodeBind])
async def bind_codes(product_data: List[ProductCodeBind], service: ProductsService = Depends(get_product_service)) -> \
        list[
            ProductCodeBind]:
    return await service.create_products(product_data)


@router.post("/aggregate", response_model=ProductAggregationResponse)
async def create_products_with_aggregation(request: ProductAggregationRequest,
                                           service: ProductsService = Depends(
                                               get_product_service)) -> ProductAggregationResponse:
    return await service.aggregate_product(request)
