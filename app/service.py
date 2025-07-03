from pprint import pprint

from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse

from utils.templates import templates
from lib.data import get_autocomplete, get_weather


class WeatherService:
    @staticmethod
    async def get_layout(request: Request, city: str | None) -> HTMLResponse:

        day_data = await get_weather(city=city, days=1, tp=1)
        pprint(day_data)
        weather_data = await get_weather(city=city, days=7, tp=24)

        if day_data.get("error") or weather_data.get("error"):
            return templates.TemplateResponse(
                request=request,
                name="not_found.htm",
                context={
                    "detail": "Please, enter correct city",
                    "link_title": "Try again",
                }
            )

        return templates.TemplateResponse(
            request=request,
            name="content.htm",
            context={
                "city": city,
                "localtime": weather_data['location']['localtime'],
                "wind": weather_data['current']['wind_kph'],
                "humidity": weather_data['current']['humidity'],
                "pressure": weather_data['current']['pressure_mb'],
                "feels_like": weather_data['current']['feelslike_c'],
                "moonrise": weather_data['forecast']['forecastday'][0]['astro']['moonrise'],
                "moonset": weather_data['forecast']['forecastday'][0]['astro']['moonset'],
                "icon": weather_data['current']['condition']['icon'],
                "week_forecast": weather_data['forecast']['forecastday'][1::],
                "day_forecast": day_data['forecast']['forecastday'][0]['hour'],
                "current_weather": weather_data['current']['condition']['text'],
                "current_temperature": weather_data['current']['temp_c'],
            }
        )

    @staticmethod
    async def autocomplete(q: str) -> JSONResponse:
        res = await get_autocomplete(query=q)
        return res
