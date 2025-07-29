from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.http_exceptions import NotFoundException, AnotherPartException
from interfaces.products_repository import IProductsRepository
from models import Batch, ProductCode
from schemas.product_codes import ProductCodeBind, ProductAggregationResponse


class ProductsRepository(IProductsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_products(self, batch_data: list[ProductCodeBind]) -> list[ProductCodeBind]:
        created = []
        for data in batch_data:
            stmt = select(Batch).filter_by(batch_number=data.batch_number, batch_date=data.batch_date)
            batch_result = await self.session.execute(stmt)
            batch = batch_result.scalar_one_or_none()
            if batch is None:
                continue
            stmt = select(ProductCode).filter_by(code=data.code)
            product_code_result = await self.session.execute(stmt)
            product_code_result = product_code_result.scalar_one_or_none()
            if product_code_result is not None:
                continue

            product = ProductCode(code=data.code, batch_id=batch.id, is_aggregated=False, aggregated_at=None)
            self.session.add(product)
            created.append({
                "code": data.code,
                "batch_number": batch.batch_number,
                "batch_date": batch.batch_date
            })
        await self.session.commit()
        return [ProductCodeBind(**item) for item in created]

    async def aggregate_product(self, batch_id: int, code: str) -> ProductAggregationResponse:
        stmt = select(ProductCode).filter_by(code=code)
        result = await self.session.execute(stmt)
        products = result.scalars().one_or_none()
        if products is None:
            raise NotFoundException('Code was not found in the database')
        if products.batch_id != batch_id:
            raise AnotherPartException("The product belong to a different batch")
        if products.is_aggregated:
            raise AnotherPartException("The product is aggregated already")
        else:
            products.aggregated_at = datetime.now()
            products.is_aggregated = True
        self.session.add(products)
        await self.session.commit()
        return ProductAggregationResponse(code=products.code, aggregated_at=products.aggregated_at)
