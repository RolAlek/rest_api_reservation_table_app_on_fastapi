from contextlib import aclosing, asynccontextmanager
from typing import Any, AsyncGenerator

from aioinject.ext.fastapi import AioInjectMiddleware
from fastapi import FastAPI

from application.api.router import main_router
from application.core import get_logger, settings
from application.core.infrastructure.di.container import init_container

logger = get_logger(__name__)


@asynccontextmanager
async def _lifespan(
    app: FastAPI,  # noqa: ARG001 - required by lifespan protocol
) -> AsyncGenerator[None, Any]:
    async with aclosing(init_container()):
        yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.api.title,
        lifespan=_lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        debug=settings.api.debug,
    )

    app.include_router(main_router)

    app.add_middleware(AioInjectMiddleware, container=init_container())

    return app
