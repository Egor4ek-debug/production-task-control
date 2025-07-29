from crud.work_center import WorkCenterRepository
from schemas.work_center import WorkCenterCreate
from models import WorkCenter

class WorkCenterService:
    def __init__(self, repo: WorkCenterRepository):
        self.repo = repo

    async def create_work_center(self, data: WorkCenterCreate) -> dict:
        return await self.repo.create_work_center(data)
