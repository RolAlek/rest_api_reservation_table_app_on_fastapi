from datetime import datetime

from application.api.schemas import BaseSchema


class TableCreateRequestSchema(BaseSchema):
    name: str
    seats: int
    location: str


class TableResponseSchema(TableCreateRequestSchema):
    id: int
    created_at: datetime
