import uvicorn

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.service import WeatherService
from app.api_v1.cities.handlers import router as city_router
from app.api_v1.histories.views import router as history_router
from app.settings import settings as s


routers_v1 = [
    city_router,
    history_router,
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


BASE_DIR = Path(__file__).resolve().parent  # папка, где лежит main.py
STATIC_DIR = BASE_DIR / "static"  # папка static внутри проекта

app = FastAPI(title="Week Weather", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

for router in routers_v1:
    app.include_router(router, prefix=s.url.api_v1_prefix)


@app.get("/")
async def root(request: Request, city: str | None = None) -> HTMLResponse:
    return await WeatherService.get_layout(request=request, city=city)


@app.get("/autocomplete")
async def autocomplete(query: str) -> JSONResponse:
    return await WeatherService.autocomplete(q=query)


@app.get("/not-found")
async def not_found(request: Request) -> HTMLResponse:
    return await WeatherService.not_found(request=request)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
