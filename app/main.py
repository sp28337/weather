from contextlib import asynccontextmanager

import uvicorn

from models import Base, db_helper
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.service import WeatherService
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils.templates import templates


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


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
