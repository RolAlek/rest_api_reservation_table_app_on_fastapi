from fastapi import FastAPI

from application.core import get_logger, settings

logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.api.title,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        debug=settings.api.debug,
    )

    return app
