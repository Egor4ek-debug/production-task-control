from fastapi import APIRouter, Depends
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from crud.product_crud import get_product_for_batch, load_existing_codes, aggregated_products
from db.session import get_async_session
from models.product_model import Product as modelProduct
from schemas.product_schemas import Product, ExistingCodesResponse, AggregatedProductsResponse, \
    AggregatedProductsRequest

router = APIRouter()


@router.post("/product", response_model=ExistingCodesResponse)
async def create_product(products: list[Product], session: AsyncSession = Depends(get_async_session)):
    mapping = await get_product_for_batch(session, products)
    print("Products keys:", {(p.batch_number, p.batch_date) for p in products})
    print("Mapping keys:", mapping.keys())
    all_codes = {p.unique_code for p in products}
    existing_codes = await load_existing_codes(session, all_codes)

    skipped_no_batch = 0  # когда не нашлось mapping
    skipped_already = 0  # когда code уже в existing_codes или повторился внутри запроса
    seen_this_request = set()
    insert_list = []

    for product in products:
        key = (product.batch_number, product.batch_date)
        batch_id = mapping.get(key)
        if batch_id is None:
            skipped_no_batch += 1
            continue

        if product.unique_code in existing_codes:
            skipped_already += 1
            continue
        if product.unique_code in seen_this_request:
            skipped_already += 1
            continue
        else:
            seen_this_request.add(product.unique_code)
            print(f'I see you {seen_this_request}')
            record = {
                "unique_code": product.unique_code,
                "batch_id": mapping.get(key),  # из mapping
                "is_aggregated": False,
                "aggregated_at": None,
            }
            insert_list.append(record)

    if insert_list:
        stmt = insert(modelProduct).values(insert_list).on_conflict_do_nothing(
            index_elements=[modelProduct.__table__.c.unique_code])
        await session.execute(stmt)
        await session.commit()
    return ExistingCodesResponse(
        inserted=len(insert_list),
        skipped_no_batch=skipped_no_batch,
        skipped_existing=skipped_already
    )


@router.post("/batches/{batch_id}/aggregated", response_model=AggregatedProductsResponse)
async def create_aggregated_product(batch_id: int, payload: AggregatedProductsRequest,
                                    session: AsyncSession = Depends(get_async_session)):
    return await aggregated_products(batch_id, payload.unique_code, session)
