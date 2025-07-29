from crud.batches import BatchRepository
from exceptions.http_exceptions import NotFoundException
from models import Batch
from schemas.batches import BatchRead, BatchCreate, BatchUpdate


class BatchService:
    def __init__(self,repo:BatchRepository):
        self.repo = repo

    async def create(self,batch_data:BatchCreate) -> BatchRead:
        batch = await self.repo.create(batch_data)
        return batch

    async def get_by_id(self,batch_id:int) -> BatchRead:
        batch = await self.repo.get_by_id(batch_id)
        if not batch:
            raise NotFoundException(detail="Batch not found")
        return batch

    async def update(self,batch_id:int,update_batch:BatchUpdate) -> Batch:
        batch = await self.repo.update(batch_id,update_data=update_batch)
        if batch is None:
            raise NotFoundException(detail="Batch not found")
        return await self.repo.update(batch_id=batch_id, update_data=update_batch)

    async def get_filtered(self,**kwargs) -> list[BatchRead]:
        return await self.repo.get_filtered(**kwargs)