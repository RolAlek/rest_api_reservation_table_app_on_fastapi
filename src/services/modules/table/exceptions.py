from dataclasses import dataclass
from typing import Any

from services.exceptions import ServiceException


@dataclass(frozen=True, eq=False)
class TableNotFoundException(ServiceException):
    table_oid: Any

    @property
    def message(self) -> str:
        return f"Table with `{self.table_oid}` id doesn't exist"
