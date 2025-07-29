from pydantic import BaseModel


class WorkCenterCreate(BaseModel):
    id: int
    name: str