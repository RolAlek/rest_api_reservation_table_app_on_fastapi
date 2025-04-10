from dataclasses import asdict

import pytest
from faker import Faker
from fastapi.encoders import jsonable_encoder

from repositories.modules.reservation.dto import CreateReservationDTO
from repositories.modules.reservation.repository import _ReservationRepository
from tests.fixtures import create_reservations  # noqa: F401


@pytest.mark.usefixtures("create_reservations")
@pytest.mark.asyncio
async def test_reservation_repository_get_list(
    reservation_repository: _ReservationRepository,
):
    result = await reservation_repository.get_all()

    assert isinstance(result, list), "Repository should return list."
    assert len(result) == 2, "Repository should return list with 2 reservations."


@pytest.mark.asyncio
async def test_reservation_repository_create(
    reservation_repository: _ReservationRepository,
    faker: Faker,
):
    empty_result = await reservation_repository.get_all()

    assert len(empty_result) == 0, "Repository should return empty list."

    dto = CreateReservationDTO(
        customer_name=faker.name(),
        reservation_time=faker.future_datetime(end_date="+10d"),
        duration_minutes=faker.random_int(),
        table_id=faker.random_int(),
    )

    result = await reservation_repository.add(dto)

    assert result.id is not None, "Repository should return reservation with id."

    result_as_dict = jsonable_encoder(result)
    result_as_dict.pop("id")
    result_as_dict.pop("created_at")

    for field in result_as_dict:
        assert field in asdict(dto).keys(), (
            f"Repository should return reservation with fields == {field}."
        )
        assert getattr(result, field) == getattr(dto, field), (
            f"Repository should return reservation with value == {getattr(dto, field)}."
        )

    result_after_creat = await reservation_repository.get_all()

    assert len(result_after_creat) == 1, (
        "Repository should return list with 1 reservation."
    )
    assert len(empty_result) < len(result_after_creat), (
        "Repository should return list with 1 reservation."
    )


@pytest.mark.usefixtures("create_reservations")
@pytest.mark.asyncio
async def test_reservation_repository_get_by_id_success(
    reservation_repository: _ReservationRepository,
):
    result = await reservation_repository.get(1)

    assert result is not None, "Repository should return reservation."
    assert result.id == 1, "Repository should return reservation with id == 1."


@pytest.mark.asyncio
async def test_reservation_repository_get_with_fake_id(
    reservation_repository: _ReservationRepository, faker: Faker
):
    result = await reservation_repository.get(faker.random_int(100))

    assert result is None, "Repository should return None."


@pytest.mark.usefixtures("create_reservations")
@pytest.mark.asyncio
async def test_reservation_repository_delete_success(
    reservation_repository: _ReservationRepository,
):
    result_before = await reservation_repository.get_all()

    assert len(result_before) == 2, "Repository should return list with 2 reservations."

    await reservation_repository.remove(result_before[0])

    result_after = await reservation_repository.get_all()

    assert len(result_after) < len(result_before), (
        "Repository should return list with 1 reservation."
    )
    assert len(result_after) == 1, "Repository should return list with 1 reservation."
