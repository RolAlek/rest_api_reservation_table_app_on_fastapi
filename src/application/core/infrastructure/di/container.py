import itertools
from collections.abc import Iterable
from functools import lru_cache

from aioinject import Container, Scoped, Singleton
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.config import APISettings, DatabaseSettings
from application.core.infrastructure.database import create_session

SETTINGS = [DatabaseSettings, APISettings]

MODULES = []


def _init_settings(
    container: Container, *, settings_classes: Iterable[type[BaseSettings]]
) -> None:
    for cls in settings_classes:
        container.register(Singleton(cls))


@lru_cache
def init_container() -> Container:
    container = Container()

    container.register(Scoped(create_session, type_=AsyncSession))

    for provider in itertools.chain.from_iterable(MODULES):
        container.register(Scoped(provider))

    _init_settings(container, settings_classes=SETTINGS)

    return container
