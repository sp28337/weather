from dataclasses import dataclass
from uuid import uuid4

from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.api_v1.histories.schemas import HistoryCreateSchema
from app.api_v1.histories.service import HistoryService
from app.api_v1.cities.service import CityService
from app.clients import get_weather_client, autocomplete_client
from app.jinja.templates import templates
from app.core.exceptions import WeatherNotFoundException


@dataclass
class WeatherService:
    history_service: HistoryService
    city_service: CityService

    async def get_layout(
        self,
        request: Request,
        city: str | None,
    ) -> HTMLResponse:

        user_id = request.cookies.get("user_id")

        if city is None and user_id is None:
            return templates.TemplateResponse(
                request=request,
                name="welcome.htm",
            )
        elif city is None and user_id:
            last_history = await self.history_service.read_last_history(user_id=user_id)
            if last_history:
                city = last_history.city
            else:
                response = templates.TemplateResponse(
                    request=request,
                    name="welcome.htm",
                )
                response.delete_cookie(user_id)
                return response
        elif user_id is None:
            user_id = str(uuid4())

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

        await self.city_service.increase_requested_field(city_name=city)
        await self.history_service.create_history(
            HistoryCreateSchema(city=city, user_id=user_id)
        )

        cities_list = await self.city_service.read_cities()
        print("cities_list")
        print(cities_list)
        histories = await self.history_service.read_user_histories(user_id=user_id)

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
