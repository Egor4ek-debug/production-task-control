from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class BatchBase(BaseModel):
    task_description: str
    shift: str
    team: str
    work_center_id: int
    is_closed: bool
    batch_number: int
    batch_date: date
    nomenclature: str
    ekn_code: str
    start_time: datetime
    end_time: datetime


class BatchCreate(BatchBase):
    pass


class BatchRead(BaseModel):
    id: int
    task_description: str
    shift: str
    team: str
    work_center_id: int
    is_closed: bool
    batch_number: int
    batch_date: date
    nomenclature: str
    ekn_code: str
    start_time: datetime
    end_time: datetime
    closed_at: Optional[datetime] = None
    product_codes: Optional[list[str]] = None

    model_config = ConfigDict(from_attributes=True)


class BatchUpdate(BaseModel):
    task_description: Optional[str] = None
    shift: Optional[str] = None
    team: Optional[str] = None
    work_center_id: Optional[int] = None
    is_closed: Optional[bool] = None
    closed_at: Optional[datetime] = None
    batch_number: Optional[int] = None
    batch_date: Optional[date] = None
    nomenclature: Optional[str] = None
    ekn_code: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
