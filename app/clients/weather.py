import httpx

from fastapi.responses import JSONResponse
from app.core.settings import settings as s
from app.core.exceptions import WeatherNotFoundException


async def get_weather_client(city: str, days: int, tp: int) -> JSONResponse:
    async with httpx.AsyncClient() as client:
        url = f"{s.weather.url}/forecast.json"
        response = await client.get(
            url,
            headers={
                "accept": "application/json",
            },
            params={
                "q": city,
                "days": days,
                "tp": tp,
                "key": s.weather.WEATHER_API_KEY,
            },
        )
        if response.status_code == 200:
            return response.json()
        raise WeatherNotFoundException


async def autocomplete_client(query: str) -> JSONResponse | dict:
    async with httpx.AsyncClient() as client:
        url = f"{s.weather.url}/search.json"
        response = await client.get(
            url, params={"key": s.weather.WEATHER_API_KEY, "q": query}
        )

        return response.json()
