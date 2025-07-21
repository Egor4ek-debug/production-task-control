from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.batch_model import Batch
from models.product_model import Product as model_product
from schemas.product_schemas import Product, AggregatedProductsResponse


async def get_product_for_batch(session: AsyncSession, products: List[Product]):
    pairs = {
        (product.batch_number, product.batch_date)
        for product in products
    }
    q = select(
        Batch
    ).where(
        tuple_(Batch.batch_number, Batch.batch_date).in_(pairs)
    ).options(
        selectinload(Batch.work_center),
        selectinload(Batch.products),
    )

    result = await session.execute(q)

    found = result.scalars().all()

    mapping = {
        (b.batch_number, b.batch_date): b.id for b in found
    }
    return mapping


async def load_existing_codes(session: AsyncSession, codes: set[str]) -> set[str]:
    q = select(model_product.unique_code).where(
        model_product.unique_code.in_(codes)
    )

    result = await session.execute(q)

    return set(result.scalars().all())


async def aggregated_products(batch_id: int, unique_code: str,
                              session: AsyncSession) -> AggregatedProductsResponse:
    product = await session.scalar(
        select(model_product)
        .filter_by(unique_code=unique_code)
    )
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product with unique code {unique_code} not found")

    if product.batch_id != batch_id:
        raise HTTPException(status_code=400, detail=f"unique code is attached to another batch")
    print("DEBUG is_aggregated BEFORE:", product.is_aggregated)
    if product.is_aggregated:
        raise HTTPException(status_code=400, detail=f"unique code already used at {product.aggregated_at}")

    product.is_aggregated = True
    product.aggregated_at = datetime.now()

    await session.commit()
    return AggregatedProductsResponse(
        unique_code=product.unique_code,
        batch_id=product.batch_id,
        is_aggregated=product.is_aggregated,
        aggregated_at=product.aggregated_at
    )
