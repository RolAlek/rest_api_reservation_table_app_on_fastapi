from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from domain.models import Base

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

engine: AsyncEngine = create_async_engine(TEST_DB_URL, echo=True)
session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory.begin() as session:
        yield session
