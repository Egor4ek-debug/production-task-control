from datetime import date, datetime

from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from models.product_model import Product
from models.work_center_model import WorkCenter


class Batch(Base):
    __tablename__ = 'batches'

    id: Mapped[int] = mapped_column(primary_key=True)
    is_closed: Mapped[bool] = mapped_column(default=False)
    task_description: Mapped[str]
    work_center: Mapped[WorkCenter] = relationship(
        'WorkCenter',
        back_populates='batches'
    )
    shift: Mapped[str]
    brigade: Mapped[str]
    batch_number: Mapped[int]
    batch_date: Mapped[date] = mapped_column(Date, nullable=False)
    nomenclature: Mapped[str]
    ekn_code: Mapped[str]
    work_center_id: Mapped[int] = mapped_column(ForeignKey('work_centers.id'), nullable=False)
    rc_identifier: Mapped[str]
    shift_start_datetime: Mapped[datetime] = mapped_column(default=datetime.now())
    shift_end_datetime: Mapped[datetime | None] = mapped_column(default=None, nullable=True)
    products: Mapped[list[Product]] = relationship(
        'Product',
        back_populates='batch'
    )
