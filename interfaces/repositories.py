from datetime import date
from typing import Protocol, Optional

from fastapi import HTTPException

from models import Batch, ProductCode, WorkCenter
from schemas.batches import BatchCreate, BatchUpdate
from schemas.product_codes import ProductCodeBind
from schemas.work_center import WorkCenterCreate


class IBatchRepository(Protocol):
    """Базовое приложение для сменных задач"""

    async def create(self, batch_data: BatchCreate) -> Batch:
        pass

    async def get_by_id(self, batch_id: int) -> Batch | None:
        pass

    async def update(self, batch_id: int, update_data: BatchUpdate) -> Batch:
        pass

    async def get_filtered(self, is_closed: Optional[bool] = None, batch_number: Optional[int] = None,
                           batch_date: Optional[date] = None,
                           work_center_id: Optional[int] = None, shift: Optional[str] = None,
                           team: Optional[str] = None, offset: int = 0,
                           limit: int = 100) -> list[Batch]:
        pass

class AppHTTPException(HTTPException):
    """Базовое приложение для исключений"""
    pass

class IProductsRepository(Protocol):
    """Базовое приложение для продуктов"""
    async def create_products(self, product_data: list[ProductCodeBind]) -> list[ProductCodeBind]:
        pass

    async def aggregate_product(self,batch_id:int,code:str) ->ProductCodeBind:
        pass

class IWorkCenterRepository(Protocol):
    """Базовое приложения для рабочего центра"""
    async def create_work_center(self, work_center_data:WorkCenterCreate) -> WorkCenter:
        pass