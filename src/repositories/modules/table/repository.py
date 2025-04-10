from dataclasses import dataclass

from domain.models.table import Table
from repositories.base import BaseSQLAlchemyRepository
from repositories.modules.table.dto import CreateTableDTO


@dataclass
class _TableRepository(BaseSQLAlchemyRepository[Table, CreateTableDTO]):
    model = Table
