from datetime import date
from typing import Protocol, Optional

from models import Batch
from schemas.batches import BatchCreate, BatchUpdate


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