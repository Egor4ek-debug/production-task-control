import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from models.work_center_model import WorkCenter
from models.product_model import Product


class BatchCreate(BaseModel):
    is_closed: bool
    task_description: str
    work_center: str
    shift: str
    brigade: str
    batch_number: int
    batch_date: datetime.date
    nomenclature: str
    ekn_code: str
    work_center_id: int
    rc_identifier: str
    shift_start_datetime: datetime.datetime
    shift_end_datetime: datetime.datetime | None

    model_config = ConfigDict(from_attributes=True)


class BatchResponse(BatchCreate):
    id: int

    @field_validator("work_center", mode="wrap")
    def _accept_work_center(cls, v, info):
        # v — то, что пришло из ORM: либо WorkCenter, либо уже str
        if isinstance(v, WorkCenter):
            return v.name
        return v


class BatchDetailResponse(BatchResponse):
    products: List[str]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("products", mode="wrap")
    def _accept_products(cls, v, info):
        if isinstance(v, Product):
            return v.unique_code
        return v


class BatchUpdate(BaseModel):
    is_closed: Optional[bool] = None
    task_description: Optional[str] = None
    work_center: Optional[str] = None
    shift: Optional[str] = None
    brigade: Optional[str] = None
    batch_number: Optional[int] = None
    batch_date: Optional[datetime.date] = None
    nomenclature: Optional[str] = None
    ekn_code: Optional[str] = None
    work_center_id: Optional[int] = None
    rc_identifier: Optional[str] = None
    shift_start_datetime: Optional[datetime.datetime] = None
    shift_end_datetime: Optional[datetime.datetime | None] = None

    model_config = ConfigDict(from_attributes=True)
