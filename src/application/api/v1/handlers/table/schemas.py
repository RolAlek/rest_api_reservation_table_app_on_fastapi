from datetime import datetime

from pydantic import PositiveInt, field_validator

from application.api.schemas import BaseSchema, ConfigDict


class TableCreateRequestSchema(BaseSchema):
    model_config = ConfigDict(str_min_length=2)

    name: str
    seats: PositiveInt
    location: str

    @field_validator("name", "location", "seats")
    def column_cant_be_null(cls, value):
        if value is None or value == "null":
            raise ValueError("Field's value cannot be null")
        return value

    @field_validator("name", "location")
    def column_cant_be_numeric(cls, value: str) -> str:
        if value.isdigit():
            raise ValueError("Field's value cannot be numeric")
        return value


class TableResponseSchema(TableCreateRequestSchema):
    id: int
    created_at: datetime
