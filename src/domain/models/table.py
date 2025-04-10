from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from domain.models.base import Base

if TYPE_CHECKING:
    from domain.models import Reservation


class Table(Base):
    name: Mapped[str]
    seats: Mapped[int]
    location: Mapped[str]

    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="table",
        cascade="delete",
        lazy="noload",
    )
