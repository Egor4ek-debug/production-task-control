from typing import List, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.work_center_model import WorkCenter
from schemas.batch_schemas import BatchCreate


async def check_exists_work_center(
        batches: List[BatchCreate],
        session: AsyncSession
) -> List[Tuple[WorkCenter, BatchCreate]]:
    results: List[Tuple[WorkCenter, BatchCreate]] = []
    for batch in batches:
        wc = await session.scalar(
            select(WorkCenter).filter_by(name=batch.work_center)
        )
        if wc is None:
            wc = WorkCenter(name=batch.work_center)
            session.add(wc)
            await session.flush()
        results.append((wc, batch))
    return results
