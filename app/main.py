import uvicorn

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.service import WeatherService
from app.api_v1 import router as router_v1
from app.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


BASE_DIR = Path(__file__).resolve().parent  # папка, где лежит main.py
STATIC_DIR = BASE_DIR / "static"  # папка static внутри проекта

app = FastAPI(title="Week Weather", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
async def root(request: Request, city: str | None = None) -> HTMLResponse:
    return await WeatherService.get_layout(request=request, city=city)


@app.get("/autocomplete")
async def autocomplete(query: str) -> JSONResponse:
    return await WeatherService.autocomplete(q=query)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
