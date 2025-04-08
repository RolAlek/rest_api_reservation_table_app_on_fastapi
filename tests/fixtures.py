import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.modules.table.dto import CreateTableDTO
from repositories.modules.table.table import _TableRepository


@pytest_asyncio.fixture
async def table_repository(get_session: AsyncSession) -> _TableRepository:
    return _TableRepository(session=get_session)


@pytest_asyncio.fixture
async def create_table(table_repository: _TableRepository, faker: Faker):
    for _ in range(2):
        dto = CreateTableDTO(
            name=faker.word(),
            seats=faker.random_int(1, 6),
            location=faker.word(),
        )
        await table_repository.add(dto)
