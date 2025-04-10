from aioinject import Scoped

from application.core.infrastructure.di._types import Providers
from repositories.base import AbstractRepository
from repositories.modules.reservation.repository import _ReservationRepository

PROVIDERS: Providers = [
    Scoped(_ReservationRepository, AbstractRepository),
]
