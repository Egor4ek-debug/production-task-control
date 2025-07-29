from fastapi import APIRouter, Depends

from deps.work_center import get_work_center_service
from schemas.work_center import WorkCenterCreate
from services.work_center import WorkCenterService

router = APIRouter(prefix="/work-centers")


@router.post("/")
async def create_work_center(work_center: WorkCenterCreate,
                             service: WorkCenterService = Depends(get_work_center_service)):
    return await service.create_work_center(work_center)
