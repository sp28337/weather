import httpx

from app.api_v1.cities.schemas import CitySchema
from app.settings import settings as s


async def create_city_client(city: str, requested: int):
    async with httpx.AsyncClient() as client:
        url = f"{s.url.protocol}://{s.url.host}:{s.url.port}{s.url.api_v1_prefix}/cities/create/"
        await client.post(
            url,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "name": city,
                "requested": requested,
            },
        )


async def get_cities_client():
    async with httpx.AsyncClient() as client:
        url = f"{s.url.protocol}://{s.url.host}:{s.url.port}{s.url.api_v1_prefix}/cities/all/"
        cities = await client.get(
            url,
            headers={
                "accept": "application/json",
            },
        )
        return cities.json()


async def get_city_by_name_client(city: str):
    async with httpx.AsyncClient() as client:
        url = f"{s.url.protocol}://{s.url.host}:{s.url.port}{s.url.api_v1_prefix}/cities/name/{city}/"
        result = await client.get(
            url,
            headers={
                "accept": "application/json",
            },
        )
        print(f"result: {result}")
        print(f"result: {result.json()}")
        return result.json()


async def update_city_partial_client(city_id):
    async with httpx.AsyncClient() as client:
        url = f"{s.url.protocol}://{s.url.host}:{s.url.port}{s.url.api_v1_prefix}/cities/update/{city_id}/"
        await client.patch(
            url,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
        )
