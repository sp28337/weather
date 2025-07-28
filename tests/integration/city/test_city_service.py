from unittest.mock import patch, AsyncMock

import pytest
from pydantic import ValidationError
from sqlalchemy import select, insert

from app.api_v1.cities.service import CityService
from app.api_v1.cities.schemas import (
    CityCreateSchema,
    CityCreateSchemaTest,
    CitySchema,
    CitySchemaTest,
)
from app.core.exceptions import CityNotFoundException


@pytest.mark.asyncio(loop_scope="session")
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
    city_service: CityService,
):
    city_data = await city_service.create_city(
        new_city=CityCreateSchemaTest(**new_city_data)
    )
    assert isinstance(city_data, CitySchema)
    assert city_data.name == new_city_data["name"]
    assert city_data.requested == new_city_data["requested"]


@pytest.mark.asyncio(loop_scope="session")
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
    city_service: CityService,
):
    with pytest.raises(ValidationError):
        CityCreateSchemaTest(**invalid_city_data)


@pytest.mark.asyncio(loop_scope="session")
async def test_read_cities__success(city_service: CityService):
    cities = await city_service.read_cities()

    assert isinstance(cities, list)
    assert len(cities) == 0

    await city_service.create_city(CityCreateSchemaTest(name="Moscow", requested=1))
    await city_service.create_city(CityCreateSchemaTest(name="Pattaya", requested=2))

    cities = await city_service.read_cities()

    assert isinstance(cities, list)
    assert cities[0].name == "Pattaya"
    assert cities[1].name == "Moscow"
    assert len(cities) == 2
    for city in cities:
        assert isinstance(city, CitySchema)
        assert isinstance(city.name, str)
        assert isinstance(city.requested, int)


@pytest.mark.asyncio(loop_scope="session")
async def test_read_city__success(
    city_service: CityService,
):
    await city_service.create_city(CityCreateSchemaTest(name="Moscow", requested=1))
    await city_service.create_city(CityCreateSchemaTest(name="Pattaya", requested=2))

    moscow = await city_service.read_city(city_id=1)
    pattaya = await city_service.read_city(city_id=2)

    assert isinstance(moscow, CitySchema)
    assert isinstance(pattaya, CitySchema)
    assert moscow.name == "Moscow"
    assert moscow.requested == 1
    assert pattaya.name == "Pattaya"
    assert pattaya.requested == 2


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "invalid_city_id",
    [-1, "10", ["10", 1, 2], 1.1, None, "", "    ", {1: 1}, (1, 2), -0.123],
)
async def test_read_city__not_found(
    invalid_city_id,
    city_service: CityService,
):
    with pytest.raises(CityNotFoundException) as error:
        await city_service.read_city(city_id=invalid_city_id)
        assert "City not found" == error.value


@pytest.mark.asyncio(loop_scope="session")
async def test_read_city_by_name__success(
    city_service: CityService,
):
    await city_service.create_city(CityCreateSchemaTest(name="Moscow", requested=1))
    await city_service.create_city(CityCreateSchemaTest(name="Pattaya", requested=2))

    moscow = await city_service.read_city_by_name(name="Moscow")
    pattaya = await city_service.read_city_by_name(name="Pattaya")

    assert isinstance(moscow, CitySchema)
    assert isinstance(pattaya, CitySchema)
    assert moscow.name == "Moscow"
    assert moscow.requested == 1
    assert pattaya.name == "Pattaya"
    assert pattaya.requested == 2


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "invalid_city_name",
    [-1, "10", ["10", 1, 2], 1.1, None, "", "   ", {1: 1}, (1, 2), -0.123, "M", 1],
)
async def test_read_city_by_name__not_found(
    invalid_city_name,
    city_service: CityService,
):
    await city_service.create_city(CityCreateSchemaTest(name="Moscow", requested=1))
    with pytest.raises(CityNotFoundException) as error:
        await city_service.read_city_by_name(name=invalid_city_name)
        assert "City not found" == error.value


@pytest.mark.asyncio(loop_scope="session")
async def test_update_city_requests_success(city_service: CityService):
    await city_service.create_city(CityCreateSchemaTest(name="Milan", requested=15))
    await city_service.create_city(CityCreateSchemaTest(name="Barcelona", requested=7))
    milan = await city_service.update_city_requests(city_id=1)
    barcelona = await city_service.update_city_requests(city_id=2)

    assert milan.name == "Milan"
    assert milan.requested == 16
    assert barcelona.name == "Barcelona"
    assert barcelona.requested == 8


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "invalid_city_id",
    [-1, "10", ["10", 1, 2], 1.1, None, "", "    ", {1: 1}, (1, 2), -0.123],
)
async def test_update_city_requests__fail(
    invalid_city_id,
    city_service: CityService,
):
    with pytest.raises(CityNotFoundException) as error:
        await city_service.update_city_requests(city_id=invalid_city_id)
        assert "City not found" == error.value


@pytest.mark.asyncio(loop_scope="session")
async def test_increase_requested_field__city_exists(
    city_service: CityService,
    city_name: str = "Bali",
) -> None:
    await city_service.create_city(CityCreateSchemaTest(name=city_name, requested=100))
    city = await city_service.read_city_by_name(name=city_name)
    if city:
        updated_city = await city_service.update_city_requests(city_id=city.id)
        assert isinstance(updated_city, CitySchema)
        assert updated_city.name == city_name
        assert updated_city.requested == 101
    else:
        pass


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "invalid_city_name",
    [-1, "10", ["10", 1, 2], 1.1, None, "", "   ", {1: 1}, (1, 2), -0.123, "M", 1],
)
async def test_increase_requested_field__city_not_exists(
    invalid_city_name,
    city_service: CityService,
) -> None:
    await city_service.create_city(CityCreateSchemaTest(name="Kazan", requested=10))
    with pytest.raises(CityNotFoundException) as error:
        city = await city_service.read_city_by_name(name=invalid_city_name)
        if city:
            pass
        else:
            assert "City not found" == error.value
            new_city = await city_service.create_city(
                CityCreateSchemaTest(name="Vladimir", requested=10)
            )
            assert new_city.requested == 1
            assert new_city.name == "Vladimir"
