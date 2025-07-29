from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from crud.work_center import WorkCenterRepository
from models import WorkCenter
from schemas.work_center import WorkCenterCreate

router = APIRouter(prefix="/work-centers")

@router.post("/")
async def create_work_center(work_center: WorkCenterCreate,session: AsyncSession = Depends(get_session)):
    repo = WorkCenterRepository(session)
    result = await repo.create_work_center(work_center)
    return result