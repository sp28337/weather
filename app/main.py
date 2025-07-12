from contextlib import asynccontextmanager

import uvicorn

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.service import WeatherService

from api_v1 import router as router_v1
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Week Weather", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
async def root(request: Request, city: str | None = None) -> HTMLResponse:
    return await WeatherService.get_layout(request=request, city=city)


@app.get("/autocomplete")
async def autocomplete(query: str) -> JSONResponse:
    return await WeatherService.autocomplete(q=query)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
