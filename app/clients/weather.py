import httpx
from dataclasses import dataclass

from fastapi.responses import JSONResponse

from app.api_v1.weatherapi.schemas import WeatherResponse
from app.core.settings import Settings
from app.core.exceptions import WeatherNotFoundException


@dataclass
class WeatherClient:
    s: Settings

    async def get_weather(self, city: str, days: int, tp: int) -> WeatherResponse:
        async with httpx.AsyncClient() as client:
            url = f"{self.s.weather.url}/forecast.json"
            response = await client.get(
                url,
                headers={
                    "accept": "application/json",
                },
                params={
                    "q": city,
                    "days": days,
                    "tp": tp,
                    "key": self.s.weather.WEATHER_API_KEY,
                },
            )
            if response.status_code == 200:
                return response.json()
            raise WeatherNotFoundException

    async def autocomplete(self, query: str) -> JSONResponse | dict:
        async with httpx.AsyncClient() as client:
            url = f"{self.s.weather.url}/search.json"
            response = await client.get(
                url, params={"key": self.s.weather.WEATHER_API_KEY, "q": query}
            )

            return response.json()
