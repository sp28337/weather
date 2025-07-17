from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure import get_session
from app.api_v1.cities.repository import CityRepository
from app.api_v1.cities.service import CityService


async def get_city_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CityRepository:
    return CityRepository(session=session)


async def get_city_service(
    city_repo: Annotated[CityRepository, Depends(get_city_repo)],
) -> CityService:
    return CityService(
        city_repo=city_repo,
    )
