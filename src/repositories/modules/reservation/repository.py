from dataclasses import dataclass

from domain.models.reservation import Reservation
from repositories.base import BaseSQLAlchemyRepository
from repositories.modules.reservation.dto import CreateReservationDTO


@dataclass
class _ReservationRepository(
    BaseSQLAlchemyRepository[Reservation, CreateReservationDTO]
):
    model = Reservation
