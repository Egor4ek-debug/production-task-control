from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class WorkCenter(Base):
    __tablename__ = 'work_centers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    batches: Mapped[list["Batch"]] = relationship('Batch', back_populates='work_center', cascade='all, delete-orphan')
