import httpx
from fastapi.responses import JSONResponse
from app.settings import settings


async def get_weather_client(city: str, days: int, tp: int) -> JSONResponse | dict:
    async with httpx.AsyncClient() as client:
        url = "https://api.weatherapi.com/v1/forecast.json"
        response = await client.get(
            url,
            headers={
                "accept": "application/json",
            },
            params={
                "q": city,
                "days": days,
                "tp": tp,
                "key": settings.WEATHER_API_KEY,
            },
        )
        return response.json()


async def autocomplete_client(query: str) -> JSONResponse | dict:
    async with httpx.AsyncClient() as client:
        url = "https://api.weatherapi.com/v1/search.json"
        response = await client.get(
            url, params={"key": settings.WEATHER_API_KEY, "q": query}
        )

        return response.json()
