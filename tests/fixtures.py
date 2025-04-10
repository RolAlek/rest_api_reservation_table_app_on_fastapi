import pytest_asyncio
from faker import Faker

from repositories.modules.reservation.dto import CreateReservationDTO
from repositories.modules.reservation.repository import _ReservationRepository
from repositories.modules.table.dto import CreateTableDTO
from repositories.modules.table.repository import _TableRepository


@pytest_asyncio.fixture
async def create_table(table_repository: _TableRepository, faker: Faker):
    for _ in range(2):
        dto = CreateTableDTO(
            name=faker.word(),
            seats=faker.random_int(1, 6),
            location=faker.word(),
        )
        await table_repository.add(dto)


@pytest_asyncio.fixture
async def create_reservations(
    reservation_repository: _ReservationRepository,
    faker: Faker,
):
    for _ in range(2):
        dto = CreateReservationDTO(
            customer_name=faker.name(),
            reservation_time=faker.future_datetime(end_date="+10d"),
            duration_minutes=faker.random_int(1, 60),
            table_id=faker.random_int(),
        )
        await reservation_repository.add(dto)
