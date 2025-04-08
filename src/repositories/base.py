from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Generic, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.base import AbstractDTO
from domain.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateData = TypeVar("CreateData", bound=AbstractDTO)


@dataclass
class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, data):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id_):
        raise NotImplementedError

    @abstractmethod
    async def remove(self, instance):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError


@dataclass
class BaseSQLAlchemyRepository(
    Generic[ModelType, CreateData],
    AbstractRepository,
):
    session: AsyncSession
    model: ModelType

    async def add(self, data: CreateData) -> ModelType:
        instance = self.model(**asdict(data))
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def get(self, id_) -> ModelType | None:
        return await self.session.get(self.model, id_)

    async def remove(self, instance: ModelType) -> None:
        await self.session.delete(instance)
        await self.session.flush()

    async def get_all(self) -> Sequence[ModelType]:
        return (await self.session.scalars(select(self.model))).all()
