from typing import Protocol

from models import WorkCenter
from schemas.work_center import WorkCenterCreate


class IWorkCenterRepository(Protocol):
    """Базовое приложения для рабочего центра"""
    async def create_work_center(self, work_center_data:WorkCenterCreate) -> WorkCenter:
        pass