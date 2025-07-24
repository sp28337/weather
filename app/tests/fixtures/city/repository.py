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
        self._cities: dict[int, CityCreateSchema] = {}
        self._next_id = 1

    async def create_city(self, new_city: CityCreateSchema) -> int:
        city_id = self._next_id
        self._cities[city_id] = CitySchema(
            id=city_id,
            name=new_city.name,
            requested=new_city.requested,
        )
        self._next_id += 1
        return city_id

    async def read_city(self, city_id: int) -> CitySchema | None:
        return self._cities.get(city_id)

    async def read_cities(self) -> list[CitySchemaBase]:
        return self._cities.values()

    @staticmethod
    async def read_city_by_name(name: str) -> None:
        return None


@pytest_asyncio.fixture
def fake_city_repository() -> FakeCityRepository:
    return FakeCityRepository()
