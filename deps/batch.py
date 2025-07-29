from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from crud.batches import BatchRepository
from services.batches import BatchService


def get_batch_repo(session: AsyncSession = Depends(get_session)) -> BatchRepository:
    return BatchRepository(session)

def get_batch_service(repo: BatchRepository = Depends(get_batch_repo)) -> BatchService:
    return BatchService(repo)