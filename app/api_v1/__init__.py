from fastapi import APIRouter

from .cities import cities_router

router = APIRouter()
router.include_router(router=cities_router, prefix="/cities")
