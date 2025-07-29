from crud.products import ProductsRepository
from schemas.product_codes import ProductCodeBind, ProductAggregationRequest

class ProductsService:
    def __init__(self, repo: ProductsRepository):
        self.repo = repo

    async def create_products(self, product_data: list[ProductCodeBind]) -> list[ProductCodeBind]:
        return await self.repo.create_products(product_data)

    async def aggregate_product(self, data: ProductAggregationRequest):
        return await self.repo.aggregate_product(batch_id=data.batch_id, code=data.code)
