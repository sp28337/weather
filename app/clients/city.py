import httpx

from app.api_v1.cities.schemas import CitySchema


async def get_cities_client():
    async with httpx.AsyncClient() as client:
        url = "http://localhost:8000/api/v1/cities/"
        cities = await client.get(
            url,
            headers={
                "accept": "application/json",
            },
        )
        return cities.json()


async def create_city_client(city: str, requested: int):
    async with httpx.AsyncClient() as client:
        url = "http://localhost:8000/api/v1/cities/"
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


async def update_city_partial_client(city: CitySchema):
    async with httpx.AsyncClient() as client:
        url = f"http://localhost:8000/api/v1/cities/{city.id}/"
        requested = city.requested + 1
        await client.patch(
            url,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "requested": requested,
            },
        )


async def get_city_by_name_client(city: str) -> CitySchema | None:
    async with httpx.AsyncClient() as client:
        url = f"http://localhost:8000/api/v1/cities/{city}/"
        result = await client.get(
            url,
            headers={
                "accept": "application/json",
            },
        )
        data = result.json()
        if data["id"] == -1:
            return None
        return CitySchema(**result.json())
