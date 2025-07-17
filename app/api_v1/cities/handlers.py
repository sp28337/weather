from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from app.exceptions import CityNotFoundException
from app.api_v1.cities.dependencies import get_city_service
from app.api_v1.cities.service import CityService
from app.api_v1.cities.schemas import (
    CitySchema,
    CityCreateSchema,
    CityUpdateSchema,
    CitySchemaBase,
)


router = APIRouter(tags=["Cities"], prefix="/cities")


@router.post(
    "/create/",
    response_model=CitySchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_city(
    new_city: CityCreateSchema,
    city_service: Annotated[CityService, Depends(get_city_service)],
):
    return await city_service.create_city(new_city=new_city)


@router.get(
    "/all/",
    response_model=list[CitySchemaBase],
)
async def read_cities(
    city_service: Annotated[CityService, Depends(get_city_service)],
):
    return await city_service.read_cities()


@router.get(
    "/id/{city_id}/",
    response_model=CitySchema,
)
async def read_city(
    city_service: Annotated[CityService, Depends(get_city_service)],
    city_id: int,
):
    try:
        return await city_service.read_city(city_id=city_id)
    except CityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail,
        )


@router.get(
    "/name/{city_name}/",
    response_model=CitySchema,
)
async def read_city_by_name(
    city_service: Annotated[CityService, Depends(get_city_service)],
    city_name: str,
):
    try:
        return await city_service.read_city_by_name(name=city_name)
    except CityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail,
        )


@router.patch("/update/{city_id}/", response_model=CityUpdateSchema)
async def update_city_requests(
    city_id: int,
    city_service: Annotated[CityService, Depends(get_city_service)],
):
    return await city_service.update_city_requests(city_id=city_id)
