from uuid import uuid4
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse

from exceptions import WeatherNotFoundException
from .jinja.templates import templates
from .actions import (
    increase_requested_city_counter,
)
from .clients import (
    get_cities_client,
    get_weather_client,
    autocomplete_client,
    get_last_history_client,
    get_histories_client,
    create_history_client,
)


class WeatherService:
    @staticmethod
    async def get_layout(
        request: Request,
        city: str | None,
    ) -> HTMLResponse:

        user_id = request.cookies.get("user_id")

        if not city and not user_id:
            return templates.TemplateResponse(
                request=request,
                name="welcome.htm",
            )
        elif not city and user_id:
            last_history = await get_last_history_client(user_id=user_id)
            city = last_history["city"]

        try:
            day_data = await get_weather_client(city=city, days=2, tp=1)
            weather_data = await get_weather_client(city=city, days=7, tp=24)
        except WeatherNotFoundException:
            return templates.TemplateResponse(
                request=request,
                name="not_found.htm",
                context={
                    "detail": "Please, enter correct city",
                    "link_title": "Try again",
                },
            )

        await increase_requested_city_counter(city=city)
        cities_list = await get_cities_client()

        histories = await get_histories_client(user_id=user_id) if user_id else None

        if not user_id:
            user_id = str(uuid4())

        await create_history_client(city=city, user_id=user_id)

        hourly_forecast = day_data["forecast"]["forecastday"][0]["hour"] + [
            day_data["forecast"]["forecastday"][1]["hour"][i] for i in range(6)
        ]

        response = templates.TemplateResponse(
            request=request,
            name="content.htm",
            context={
                "histories": histories,
                "cities_list": cities_list,
                "city": city,
                "code": weather_data["current"]["condition"]["code"],
                "localtime": weather_data["location"]["localtime"],
                "wind": weather_data["current"]["wind_kph"],
                "humidity": weather_data["current"]["humidity"],
                "pressure": weather_data["current"]["pressure_mb"],
                "feels_like": weather_data["current"]["feelslike_c"],
                "moonrise": weather_data["forecast"]["forecastday"][0]["astro"][
                    "moonrise"
                ],
                "moonset": weather_data["forecast"]["forecastday"][0]["astro"][
                    "moonset"
                ],
                "icon": weather_data["current"]["condition"]["icon"],
                "week_forecast": weather_data["forecast"]["forecastday"][1::],
                "day_forecast": hourly_forecast,
                "current_weather": weather_data["current"]["condition"]["text"],
                "current_temperature": weather_data["current"]["temp_c"],
            },
        )

        response.set_cookie(
            key="user_id", value=user_id, httponly=False, max_age=604800 * 5200
        )

        return response

    @staticmethod
    async def autocomplete(q: str) -> JSONResponse:
        res = await autocomplete_client(query=q)
        return res

    @staticmethod
    async def not_found(
        request: Request,
    ) -> HTMLResponse:
        response = templates.TemplateResponse(
            request=request,
            name="not_found.htm",
            context={
                "detail": "Please, enter correct city",
                "link_title": "Try again",
            },
        )
        return response
