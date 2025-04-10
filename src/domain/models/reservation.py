from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.models.base import Base

if TYPE_CHECKING:
    from domain.models import Table


class Reservation(Base):
    customer_name: Mapped[str] = mapped_column(String(128))
    reservation_time: Mapped[datetime]
    duration_minutes: Mapped[int]

    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    table: Mapped["Table"] = relationship(back_populates="reservations")
