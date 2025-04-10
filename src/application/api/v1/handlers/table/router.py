from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, HTTPException, status

from application.api.v1.handlers.table.schemas import (
    TableCreateRequestSchema, TableResponseSchema)
from repositories.modules.table.dto import CreateTableDTO
from services.exceptions import ServiceException
from services.modules.table.service import TableService

router = APIRouter()


@router.get("/", response_model=list[TableResponseSchema])
@inject
async def get_all_tables(service: Injected["TableService"]):
    return await service.get_all()


@router.post(
    "/",
    response_model=TableResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_new_table(
    schema: TableCreateRequestSchema,
    service: Injected["TableService"],
):
    new_table = await service.create(
        CreateTableDTO(**schema.model_dump(exclude_unset=True))
    )
    return new_table


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_table(table_id: int, service: Injected["TableService"]):
    try:
        await service.delete(table_id)
    except ServiceException as exception:
        raise HTTPException(
            status_code=404,
            detail=exception.message,
        ) from exception
