from contextlib import asynccontextmanager

import uvicorn

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.service import WeatherService
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils.templates import templates
from api_v1 import router as router_v1
from settings import Settings

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router_v1, prefix=settings.api_v1_prefix)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return templates.TemplateResponse(
        request=request,
        name="not_found.htm",
        context={
            "detail": "Page not found",
            "link_title": "Go to homepage",
        },
    )


@app.get("/")
async def root(request: Request, city: str | None = "Pattaya") -> HTMLResponse:
    return await WeatherService.get_layout(request=request, city=city)


@app.get("/autocomplete")
async def autocomplete(query: str) -> JSONResponse:
    return await WeatherService.autocomplete(q=query)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
