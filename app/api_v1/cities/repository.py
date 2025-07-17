from sqlalchemy import select, desc, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.cities.schemas import CityUpdateSchema
from app.models import City


class CityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_city(
        self,
        new_city: City,
    ) -> int:
        city = City(
            name=new_city.name,
            requested=new_city.requested,
        )
        self.session.add(city)
        await self.session.flush()
        city_id = city.id
        await self.session.commit()
        # await self.session.refresh(city)
        return city_id

    async def read_cities(self) -> list[City]:
        stmt = select(City).order_by(desc(City.requested)).limit(10)
        result: Result = await self.session.execute(stmt)
        cities = result.scalars().all()
        return cities

    async def read_city(self, city_id: int) -> City | None:
        # return await session.get(City, city_id)
        stmt = select(City).where(City.id == city_id)
        city: City | None = await self.session.scalar(stmt)
        return city

    async def read_city_by_name(self, name: str) -> City | None:
        stmt = select(City).where(City.name == name)
        city: City | None = await self.session.scalar(stmt)
        return city

    # async def update_city(
    #     self,
    #     city: City,
    #     city_update: CityUpdateSchema | CityUpdatePartialSchema,
    #     partial: bool = False,
    # ) -> City:
    #     for name, value in city_update.model_dump(exclude_unset=partial).items():
    #         setattr(city, name, value)
    #     await self.session.commit()
    #     return city

    async def update_city_requests(self, city_id: int) -> City:
        stmt = (
            update(City)
            .where(City.id == city_id)
            .values(requested=City.requested + 1)
            .returning(City.id)
        )
        result = await self.session.execute(stmt)
        city_id = result.scalar_one()

        await self.session.commit()
        await self.session.flush()
        return await self.read_city(city_id)
