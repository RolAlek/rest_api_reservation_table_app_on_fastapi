from dataclasses import dataclass

from repositories.values import AbstractDTO


@dataclass
class CreateTableDTO(AbstractDTO):
    name: str
    seats: int
    location: str
