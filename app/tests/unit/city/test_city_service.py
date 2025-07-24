import pytest

from unittest.mock import patch, AsyncMock
from pydantic import ValidationError
from app.api_v1.cities.service import CityService
from app.api_v1.cities.schemas import (
    CityCreateSchema,
    CitySchema,
    CityCreateSchemaTest,
    CitySchemaBase,
)


pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "new_city_data",
    [
        {"name": "Moscow", "requested": 1},
        {"name": "Moscow" * 10, "requested": 1},
        {"name": "New York", "requested": 777},
        {"name": "LA", "requested": 5},
    ],
)
async def test_create_city__success(
    new_city_data,
    mock_city_service: CityService,
):
    new_city = CityCreateSchema(**new_city_data)
    result = await mock_city_service.create_city(new_city=new_city)
    assert isinstance(result, CitySchema)
    assert result.name == new_city_data["name"]
    assert result.requested == new_city_data["requested"]


@pytest.mark.parametrize(
    "invalid_city_data",
    [
        {"name": "", "requested": 5},
        {"name": "A", "requested": 2},
        {"name": "Moscow", "requested": "2"},
        {"name": 1, "requested": 7},
        {"name": ["Moscow"], "requested": 1},
        {"name": "Moscow", "requested": 3.14},
        {"name": None, "requested": 1},
        {"name": "Moscow", "requested": None},
        {},
        {"requested": 5},
        {"name": "Moscow"},
        {"name": " " * 10, "requested": 1},
        {"name": "ValidName", "requested": -1},
    ],
)
async def test_create_city__fail(
    invalid_city_data,
    mock_city_service: CityService,
):
    with pytest.raises(ValidationError):
        CityCreateSchemaTest(**invalid_city_data)


async def test_read_cities__success(mock_city_service: CityService):
    cities = await mock_city_service.read_cities()

    assert isinstance(cities, list)
    assert len(cities) == 0

    await mock_city_service.create_city(
        CityCreateSchemaTest(name="Moscow", requested=1)
    )
    await mock_city_service.create_city(
        CityCreateSchemaTest(name="Pattaya", requested=1)
    )

    cities = await mock_city_service.read_cities()

    assert isinstance(cities, list)
    assert cities[0].name == "Moscow"
    assert cities[1].name == "Pattaya"
    assert len(cities) == 2
    for city in cities:
        assert isinstance(city, CitySchemaBase)
        assert isinstance(city.name, str)
        assert isinstance(city.requested, int)


@pytest.mark.asyncio
async def test_read_cities__validation_fail(mock_city_service: CityService):
    invalid_data = [object()]

    with patch.object(
        mock_city_service.city_repo,
        "read_cities",
        new_callable=AsyncMock,
    ) as mock_repo:
        mock_repo.return_value = invalid_data

        with pytest.raises(ValidationError):
            await mock_city_service.read_cities()


@pytest.mark.asyncio
async def test_read_cities__repository_throws(mock_city_service: CityService):
    with patch.object(
        mock_city_service.city_repo, "read_cities", new_callable=AsyncMock
    ) as mock_repo:
        mock_repo.side_effect = RuntimeError("DB connection error")

        with pytest.raises(RuntimeError):
            await mock_city_service.read_cities()
