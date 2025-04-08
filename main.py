import uvicorn

from src.application.core import get_logger, settings

logger = get_logger(__name__)

if __name__ == "__main__":
    uvicorn.run(
        "src.application.app:create_app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.api.debug,
        factory=True,
    )
