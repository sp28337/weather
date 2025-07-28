import pytest_asyncio

from dataclasses import dataclass

from app.api_v1.cities.schemas import (
    CityCreateSchema,
    CitySchema,
    CitySchemaBase,
)


@dataclass
class FakeCityRepository:
    def __init__(self):
        self._cities_id_keys: dict[int, CitySchema] = {}
        self._cities_name_keys: dict[str, CitySchema] = {}
        self._next_id = 1

    async def create_city(self, new_city: CityCreateSchema) -> int:
        city_id = self._next_id
        self._cities_id_keys[city_id] = CitySchema(
            id=city_id,
            name=new_city.name,
            requested=new_city.requested,
        )
        self._cities_name_keys[new_city.name] = CitySchema(
            id=city_id,
            name=new_city.name,
            requested=new_city.requested,
        )
        self._next_id += 1
        return city_id

    async def read_cities(self) -> list[CitySchemaBase]:
        return self._cities_id_keys.values()

    async def read_city(self, city_id: int) -> CitySchema | None:
        return self._cities_id_keys.get(city_id)

    async def read_city_by_name(self, name: str) -> CitySchema | None:
        return self._cities_name_keys.get(name)

    async def update_city_requests(self, city_id: int) -> int:
        city_for_update = self._cities_id_keys.get(city_id)
        city_for_update.requested += 1
        return city_id


@pytest_asyncio.fixture
def fake_city_repository() -> FakeCityRepository:
    return FakeCityRepository()
