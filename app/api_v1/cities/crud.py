from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from models.city import City
from api_v1.cities import (
    CityCreateSchema,
    CityUpdateSchema,
    CityUpdatePartialSchema,
)


async def get_cities(session: AsyncSession) -> list[City]:
    stmt = select(City).order_by(City.id)
    result: Result = await session.execute(stmt)
    cities = result.scalars().all()
    return cities


async def get_city(session: AsyncSession, city_id: int) -> City | None:
    return await session.get(City, city_id)


async def create_city(
    session: AsyncSession,
    new_city: CityCreateSchema,
) -> City:
    city = City(**new_city.model_dump())
    session.add(city)
    await session.commit()
    # await session.refresh(city)
    return city


async def update_city(
    session: AsyncSession,
    city: City,
    city_update: CityUpdateSchema | CityUpdatePartialSchema,
    partial: bool = False,
) -> City:
    for name, value in city_update.model_dump(exclude_unset=partial).items():
        setattr(city, name, value)
    await session.commit()
    return city


async def delete_city(
    session: AsyncSession,
    city: City,
) -> None:
    await session.delete(city)
    await session.commit()
