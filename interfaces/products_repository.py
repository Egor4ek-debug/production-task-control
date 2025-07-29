from typing import Protocol

from schemas.product_codes import ProductCodeBind


class IProductsRepository(Protocol):
    """Базовое приложение для продуктов"""
    async def create_products(self, product_data: list[ProductCodeBind]) -> list[ProductCodeBind]:
        pass

    async def aggregate_product(self,batch_id:int,code:str) ->ProductCodeBind:
        pass