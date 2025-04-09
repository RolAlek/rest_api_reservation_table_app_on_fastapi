from dataclasses import dataclass
from typing import Sequence

from domain.models.table import Table
from repositories.base import AbstractRepository
from repositories.modules.table.dto import CreateTableDTO
from repositories.modules.table.table import _TableRepository
from services.base import AbstractService
from services.modules.table.exceptions import TableNotFoundException


@dataclass
class TableService(AbstractService):
    repository: AbstractRepository = _TableRepository

    async def get_all(self) -> Sequence[Table]:
        result = await self.repository.get_all()

        return result

    async def create(self, data: CreateTableDTO) -> Table:
        result = await self.repository.add(data)

        return result

    async def delete(self, oid: int):
        instance = await self.repository.get(oid)

        if instance is None:
            raise TableNotFoundException(oid)

        await self.repository.remove(instance)
