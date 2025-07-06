from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from models import db_helper
from . import crud
from .schemas import (
    CitySchema,
    CityCreateSchema,
    CityUpdatePartialSchema,
    CityUpdateSchema,
    CitySchemaBase,
)
from .dependencies import get_city_by_id, get_city_by_name


router = APIRouter(tags=["Cities"])


@router.get("/", response_model=list[CitySchemaBase])
async def get_cities(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_cities(session=session)


@router.post(
    "/",
    response_model=CitySchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_city(
    new_city: CityCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_city(session=session, new_city=new_city)


@router.get("/{city_name}/", response_model=CitySchema)
async def get_city_by_name(
    city: CitySchema = Depends(get_city_by_name),
):
    return city


@router.get("/{city_id}/", response_model=CitySchema)
async def get_city(
    city: CitySchema = Depends(get_city_by_id),
):
    return city


@router.put("/{city_id}/")
async def update_city(
    city_update: CityUpdateSchema,
    city: CitySchema = Depends(get_city_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_city(
        session=session,
        city=city,
        city_update=city_update,
    )


@router.patch("/{city_id}/")
async def update_city_partial(
    city_update: CityUpdatePartialSchema,
    city: CitySchema = Depends(get_city_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_city(
        session=session,
        city=city,
        city_update=city_update,
        partial=True,
    )


@router.delete("/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
    city: CitySchema = Depends(get_city_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_city(session=session, city=city)
