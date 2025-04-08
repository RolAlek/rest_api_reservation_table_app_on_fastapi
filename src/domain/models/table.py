from sqlalchemy.orm import Mapped

from domain.models.base import Base


class Table(Base):
    name: Mapped[str]
    seats: Mapped[int]
    location: Mapped[str]
