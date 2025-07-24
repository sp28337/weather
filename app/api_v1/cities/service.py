from dataclasses import dataclass

from app.core.exceptions import CityNotFoundException
from app.api_v1.cities.schemas import (
    CitySchema,
    CityCreateSchema,
    CitySchemaBase,
    CityUpdateSchema,
)
from app.api_v1.cities.repository import CityRepository


@dataclass
class CityService:
    city_repo: CityRepository

    async def create_city(self, new_city: CityCreateSchema) -> CitySchema:
        city_id = await self.city_repo.create_city(new_city=new_city)
        city = await self.city_repo.read_city(city_id)
        return CitySchema.model_validate(city)

    async def read_cities(self) -> list[CitySchemaBase]:
        cities = await self.city_repo.read_cities()
        cities_list = [CitySchemaBase.model_validate(city) for city in cities]
        return cities_list

    async def read_city(self, city_id: int) -> CitySchema:
        if not isinstance(city_id, int) or city_id <= 0:
            raise CityNotFoundException

        city = await self.city_repo.read_city(city_id=city_id)

        if city is None:
            raise CityNotFoundException

        response = CitySchema.model_validate(city)
        return response

    async def read_city_by_name(self, name: str) -> CitySchema:
        city = await self.city_repo.read_city_by_name(name=name)
        if city is None:
            raise CityNotFoundException

        response = CitySchema.model_validate(city)
        return response

    async def update_city_requests(self, city_id: int) -> CitySchema:
        updated_city = await self.city_repo.update_city_requests(city_id=city_id)
        return CityUpdateSchema.model_validate(updated_city)

    async def increase_requested_field(self, city: str) -> None:
        city = await self.read_city_by_name(name=city)
        if city:
            await self.update_city_requests(city_id=city.id)
        else:
            await self.create_city(CityCreateSchema(name=city, requested=1))
