from datetime import date, datetime

from pydantic import BaseModel


class ProductCodeBind(BaseModel):
    code:str
    batch_number:int
    batch_date:date

    class Config:
        from_attributes = True

class ProductAggregationRequest(BaseModel):
    batch_id:int
    code:str

class ProductAggregationResponse(BaseModel):
    code:str
    aggregated_at:datetime