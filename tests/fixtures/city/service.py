import pytest_asyncio

from app.api_v1.cities.repository import CityRepository
from app.api_v1.cities.service import CityService


@pytest_asyncio.fixture
def mock_city_service(
    fake_city_repository,
):
    return CityService(
        city_repo=fake_city_repository,
    )


@pytest_asyncio.fixture
def city_service(
    get_db_session,
):
    return CityService(
        city_repo=CityRepository(session=get_db_session),
    )
