from aioinject import Scoped

from application.core.infrastructure.di._types import Providers
from repositories.base import AbstractRepository
from repositories.modules.table.table import _TableRepository
from services.modules.table.service import TableService

PROVIDERS: Providers = [
    Scoped(_TableRepository, AbstractRepository),
    Scoped(TableService),
]
