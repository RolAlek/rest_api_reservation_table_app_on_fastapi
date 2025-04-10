from contextlib import asynccontextmanager
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from aioinject import Container, Scoped
from aioinject.ext.fastapi import AioInjectMiddleware
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from application.app import create_app
from application.core.infrastructure.di.container import init_container
from domain.models import Base
from repositories.modules.reservation.repository import _ReservationRepository
from repositories.modules.table.repository import _TableRepository
from services.modules.table.service import TableService

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

engine: AsyncEngine = create_async_engine(
    TEST_DB_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)
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


@asynccontextmanager
async def test_session_dependency() -> AsyncGenerator[AsyncSession]:
    async with session_factory.begin() as session:
        yield session


@pytest_asyncio.fixture
async def table_repository(get_session: AsyncSession) -> _TableRepository:
    return _TableRepository(session=get_session)


@pytest_asyncio.fixture
async def table_service(table_repository: _TableRepository) -> TableService:
    return TableService(table_repository)


@pytest_asyncio.fixture
async def reservation_repository(get_session: AsyncSession) -> _ReservationRepository:
    return _ReservationRepository(session=get_session)


@pytest.fixture
def test_container() -> Container:
    container = init_container()

    container.try_register(Scoped(test_session_dependency, type_=AsyncSession))
    return container


@pytest.fixture
def app(test_container: Container) -> FastAPI:
    app = create_app()
    app.add_middleware(AioInjectMiddleware, container=test_container)
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
