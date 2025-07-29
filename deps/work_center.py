from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_session
from crud.work_center import WorkCenterRepository
from services.work_center import WorkCenterService

def get_work_center_repo(session: AsyncSession = Depends(get_session)) -> WorkCenterRepository:
    return WorkCenterRepository(session)

def get_work_center_service(repo: WorkCenterRepository = Depends(get_work_center_repo)) -> WorkCenterService:
    return WorkCenterService(repo)
