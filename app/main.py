import uvicorn
from typing import Annotated

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse

from app.api_v1.weatherapi.service import WeatherService
from app.api_v1.cities.handlers import router as city_router
from app.api_v1.histories.handlers import router as history_router
from app.api_v1.weatherapi.handlers import router as weatherapi_router
from app.core.settings import settings as s
from app.core.dependencies import get_weather_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


BASE_DIR = Path(__file__).resolve().parent  # папка, где лежит main.py
STATIC_DIR = BASE_DIR / "static"  # папка static внутри проекта

app = FastAPI(title="Week Weather", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

routers_v1 = [
    city_router,
    history_router,
]

for router in routers_v1:
    app.include_router(router, prefix=s.url.api_v1_prefix)
else:
    app.include_router(weatherapi_router)


@app.get("/not-found")
async def not_found(
    request: Request,
    weather_service: Annotated[WeatherService, Depends(get_weather_service)],
) -> HTMLResponse:
    return await weather_service.not_found(request=request)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
