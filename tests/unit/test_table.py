import pytest
from faker import Faker

from repositories.modules.table.dto import CreateTableDTO
from repositories.modules.table.table import _TableRepository
from services.modules.table.exceptions import TableNotFoundException
from services.modules.table.service import TableService
from tests.fixtures import create_table, table_repository, table_service  # noqa


@pytest.mark.asyncio
async def test_repository_add_table_in_db(
    table_repository: _TableRepository,
    faker: Faker,
):
    table_data = CreateTableDTO(
        name=faker.word(),
        seats=faker.random_int(),
        location=faker.word(),
    )
    created_table = await table_repository.add(table_data)

    assert created_table is not None
    response = await table_repository.get_all()

    assert len(response) == 1, "Table should be created in db"
    assert created_table in response, "Table should be in db"


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_table")
async def test_repository_get_all_tables(table_repository: _TableRepository):
    tables = await table_repository.get_all()

    assert isinstance(tables, list), "Should return a list of tables objects"
    assert len(tables) == 2, "Should return 2 tables"


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_table")
async def test_repository_delete_table_success(table_repository: _TableRepository):
    tables = await table_repository.get_all()

    table_for_delete = tables[0]

    await table_repository.remove(table_for_delete)

    tables_after_delete = await table_repository.get_all()

    assert len(tables_after_delete) == 1, "Should return 1 table after deletion"
    assert table_for_delete not in tables_after_delete, (
        f"Should not contain deleted `{table_for_delete.id}` table"
    )
    assert await table_repository.get(table_for_delete.id) is None, (
        "Should return None after deletion"
    )


@pytest.mark.asyncio
async def test_repository_get_table_with_not_existing_id(
    table_repository: _TableRepository,
):
    result = await table_repository.get(100)

    assert result is None, "Should return None if table not exists"


@pytest.mark.asyncio
async def test_service_create_table_success(table_service: TableService, faker: Faker):
    dto = CreateTableDTO(
        name=faker.word(),
        seats=faker.random_int(),
        location=faker.word(),
    )

    empty_result = await table_service.get_all()

    assert len(empty_result) == 0, "Should return an empty list"

    created_table = await table_service.create(dto)

    result_after_create = await table_service.get_all()

    assert len(empty_result) < len(result_after_create), (
        "Result after create should be bigger than empty"
    )
    assert len(result_after_create) == 1, "Should return a list of tables objects"
    assert created_table in result_after_create, "Table should exists in db"


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_table")
async def test_service_get_all_tables(table_service: TableService):
    result = await table_service.get_all()

    assert isinstance(result, list), "Should return a list of tables objects"
    assert len(result) == 2, "Result should be contains 2 tables"


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_table")
async def test_service_delete_table_success(
    table_service: TableService,
    table_repository: _TableRepository,
):
    result_before_delete = await table_service.get_all()

    assert len(result_before_delete) == 2, "Should return 2 tables"

    await table_service.delete(1)

    result_after_delete = await table_service.get_all()

    assert len(result_before_delete) > len(result_after_delete), (
        "Result after delete should be less than before"
    )
    assert len(result_after_delete) == 1, "Should return a list with 1 table"
    assert await table_repository.get(1) is None, "Table with id 1 should be deleted"


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_table")
async def test_service_rased_exception_on_delete_with_not_existing_id(
    table_service: TableService,
):
    result_before_delete = await table_service.get_all()

    assert len(result_before_delete) == 2, "Should return 2 tables"

    with pytest.raises(TableNotFoundException):
        await table_service.delete(100)

    result_after_delete = await table_service.get_all()

    assert len(result_after_delete) == 2, "Should return a list with 2 tables"
    assert len(result_before_delete) == len(result_after_delete), (
        "Result should not change"
    )
