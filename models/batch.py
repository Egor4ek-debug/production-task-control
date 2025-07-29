from datetime import datetime, date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Batch(Base):
    __tablename__ = 'batches'
    id: Mapped[int] = mapped_column(primary_key=True)
    task_description: Mapped[str] = mapped_column(default='')
    shift: Mapped[str] = mapped_column(default='')
    team: Mapped[str] = mapped_column(default='')
    work_center_id: Mapped[int] = mapped_column(ForeignKey('work_centers.id'))
    is_closed: Mapped[bool] = mapped_column(default=False)
    closed_at: Mapped[datetime] = mapped_column(default=None, nullable=True)
    batch_number: Mapped[int] = mapped_column(default=0)
    batch_date: Mapped[date] = mapped_column(default=None, nullable=True)
    nomenclature: Mapped[str] = mapped_column(default='')
    ekn_code: Mapped[str] = mapped_column(default='')
    start_time: Mapped[datetime] = mapped_column(default=None, nullable=True)
    end_time: Mapped[datetime] = mapped_column(default=None, nullable=True)

    work_center: Mapped["WorkCenter"] = relationship("WorkCenter", back_populates="batches")
    product_codes: Mapped[list["ProductCode"]] = relationship("ProductCode", back_populates="batch", lazy="selectin")
