from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse

from app.api_v1.weatherapi.service import WeatherService
from app.core.dependencies import get_weather_service


router = APIRouter()


@router.get("/")
async def root(
    request: Request,
    weather_service: Annotated[WeatherService, Depends(get_weather_service)],
    city: str | None = None,
) -> HTMLResponse:
    return await weather_service.get_layout(
        request=request,
        city=city,
    )


@router.get("/autocomplete")
async def autocomplete(
    query: str,
    weather_service: Annotated[WeatherService, Depends(get_weather_service)],
) -> JSONResponse:
    return await weather_service.autocomplete(
        q=query,
    )
