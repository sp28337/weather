import pytest_asyncio

from app.api_v1.cities.service import CityService


@pytest_asyncio.fixture
def mock_city_service(
    fake_city_repository,
):
    return CityService(
        city_repo=fake_city_repository,
    )
