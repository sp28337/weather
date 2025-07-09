from fastapi import APIRouter

from .cities import cities_router
from .histories import history_router

router = APIRouter()
router.include_router(router=cities_router, prefix="/cities")
router.include_router(router=history_router, prefix="/histories")
