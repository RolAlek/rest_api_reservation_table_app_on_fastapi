from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from repositories.values import AbstractDTO


@dataclass
class AbstractService(ABC):
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def create(self, data: AbstractDTO):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, oid: Any):
        raise NotImplementedError
