from dataclasses import dataclass
from datetime import datetime

from repositories.values import AbstractDTO


@dataclass
class CreateReservationDTO(AbstractDTO):
    customer_name: str
    reservation_time: datetime
    duration_minutes: int
    table_id: int
