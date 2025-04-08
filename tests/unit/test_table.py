import pytest

from repositories.modules.table.dto import CreateTableDTO
from repositories.modules.table.table import _TableRepository
from tests.fixtures import create_table, table_repository  # noqa


@pytest.mark.asyncio
async def test_add_table_in_db(table_repository: _TableRepository):
    table_data = CreateTableDTO(name="test", seats=2, location="test")
    created_table = await table_repository.add(table_data)

    assert created_table is not None
    response = await table_repository.get_all()

    assert len(response) == 1, "Table should be created in db"
    assert created_table in response, "Table should be in db"


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_table")
async def test_get_all_tables(table_repository: _TableRepository):
    tables = await table_repository.get_all()

    assert isinstance(tables, list), "Should return a list of tables objects"
    assert len(tables) == 2, "Should return 2 tables"


@pytest.mark.asyncio
@pytest.mark.usefixtures("create_table")
async def test_delete_table(table_repository: _TableRepository):
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
async def test_get_table_with_not_existing_id(table_repository: _TableRepository):
    result = await table_repository.get(100)

    assert result is None, "Should return None if table not exists"
