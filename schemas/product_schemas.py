from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    unique_code: str
    batch_number: int
    batch_date: date

    model_config = ConfigDict(from_attributes=True)


class ExistingCodesResponse(BaseModel):
    inserted: int
    skipped_no_batch: int
    skipped_existing: int


class AggregatedProductsRequest(BaseModel):
    unique_code: str


class AggregatedProductsResponse(BaseModel):
    unique_code: str
    batch_id: int
    is_aggregated: bool
    aggregated_at: datetime
