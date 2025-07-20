from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure import get_session
from app.api_v1.histories.repository import HistoryRepository
from app.api_v1.histories.service import HistoryService
from app.api_v1.weatherapi.service import WeatherService
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


async def get_history_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> HistoryRepository:
    return HistoryRepository(session=session)


async def get_history_service(
    history_repo: Annotated[HistoryRepository, Depends(get_history_repo)],
) -> HistoryService:
    return HistoryService(
        history_repo=history_repo,
    )


async def get_weather_service(
    history_service: Annotated[HistoryService, Depends(get_history_service)],
    city_service: Annotated[CityService, Depends(get_city_service)],
) -> WeatherService:

    return WeatherService(
        history_service=history_service,
        city_service=city_service,
    )
