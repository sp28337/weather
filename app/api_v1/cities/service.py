from dataclasses import dataclass

from app.exceptions import CityNotFoundException
from .schemas import (
    CitySchema,
    CityCreateSchema,
    CitySchemaBase,
    CityUpdateSchema,
)
from .repository import CityRepository


@dataclass
class CityService:
    city_repo: CityRepository

    async def create_city(self, new_city: CityCreateSchema) -> CitySchema:
        city_id = await self.city_repo.create_city(new_city=new_city)
        city = await self.city_repo.read_city(city_id)
        return CitySchema.model_validate(city)

    async def read_cities(self) -> list[CitySchemaBase]:
        cities = await self.city_repo.read_cities()
        cities_schema = [CitySchema.model_validate(city) for city in cities]
        return cities_schema

    async def read_city(self, city_id: int) -> CitySchema:
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

        # if city is not None:
        #     return city
        # return {
        #     "id": -1,
        #     "name": "",
        #     "requested": 0,
        # }

        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND,
        #     detail=f"City {city_name} not found!",
        # )

    async def update_city_requests(self, city_id: int) -> CitySchema:
        updated_city = await self.city_repo.update_city_requests(city_id=city_id)
        return CityUpdateSchema.model_validate(updated_city)
