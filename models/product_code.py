from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class ProductCode(Base):
    __tablename__ = 'product_codes'

    id:Mapped[int] = mapped_column(primary_key=True)
    code:Mapped[str] = mapped_column(unique=True)
    is_aggregated:Mapped[bool] = mapped_column(default=False)
    aggregated_at:Mapped[datetime|None] = mapped_column(nullable=True,default=None)
    batch_id:Mapped[int] = mapped_column(ForeignKey('batches.id'))

    batch:Mapped["Batch"] = relationship("Batch",back_populates="product_codes",lazy='selectin')
