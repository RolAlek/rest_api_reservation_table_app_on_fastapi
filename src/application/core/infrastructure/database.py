from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from application.core import settings

engine: AsyncEngine = create_async_engine(
    settings.db.url,
    echo=settings.db.echo,
)

session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)


@asynccontextmanager
async def create_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory.begin() as session:
        yield session
