from sqlalchemy.ext.asyncio import AsyncSession

from models import WorkCenter
from schemas.work_center import WorkCenterCreate


class WorkCenterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_work_center(self, work_center: WorkCenterCreate):
        wc = WorkCenter(id=work_center.id, name=work_center.name)
        self.session.add(wc)
        await self.session.commit()
        await self.session.refresh(wc)
        return {"id": wc.id, "name": wc.name}
