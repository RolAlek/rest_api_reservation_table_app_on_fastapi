from fastapi import APIRouter

from .handlers.table.router import router as table_router

router = APIRouter()
router.include_router(table_router, prefix="/tables", tags=["Tables"])
