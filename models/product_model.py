import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    unique_code: Mapped[str] = mapped_column(unique=True)
    batch_id: Mapped[int] = mapped_column(ForeignKey('batches.id'))
    is_aggregated: Mapped[bool] = mapped_column(default=False)
    aggregated_at: Mapped[Optional[datetime.datetime]] = mapped_column(default=None)

    batch: Mapped["Batch"] = relationship("Batch", back_populates="products")
