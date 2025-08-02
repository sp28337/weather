import pytest

from fastapi.responses import JSONResponse
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import Response, Request

from app.core.exceptions import WeatherNotFoundException
from app.core.settings import Settings
from app.clients import WeatherClient
from app.api_v1.weatherapi.service import WeatherService


pytestmark = pytest.mark.asyncio


async def test_get_weather__success():
    settings = Settings()
    settings.weather = type("WeatherSettings", (), {})()
    settings.weather.url = "https://fake-weather-api.com"
    settings.weather.WEATHER_API_KEY = "fakeapikey"

    client = WeatherClient(s=settings)

    data = {"location": {"name": "Moscow"}, "current": {"temp_c": 10}}

    mock_client_instance = AsyncMock()
    mock_client_instance.get.return_value = Response(
        status_code=200,
        request=Request("GET", url="https://fake-weather-api.com/forecast.json"),
        json=data,
    )

    mock_async_client = AsyncMock()
    mock_async_client.__aenter__.return_value = mock_client_instance
    mock_async_client.__aexit__.return_value = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_async_client):
        result = await client.get_weather(city="Moscow", days=2, tp=1)

    assert result == data


async def test_get_weather__fail():
    settings = Settings()
    settings.weather = type("WeatherSettings", (), {})()
    settings.weather.url = "https://fake-weather-api.com"
    settings.weather.WEATHER_API_KEY = "fakeapikey"

    client = WeatherClient(s=settings)

    async_mock = AsyncMock()
    async_mock.get.return_value = Response(
        status_code=404,
        request=Request("GET", url="https://fake-weather-api.com/forecast.json"),
        json={"error": "not found"},
    )
    with patch("httpx.AsyncClient", return_value=async_mock):
        with pytest.raises(WeatherNotFoundException):
            await client.get_weather(city="InvalidCity", days=2, tp=1)


async def test_autocomplete__success():
    mock_weather_client = MagicMock()
    mock_weather_client.autocomplete = AsyncMock(
        return_value=JSONResponse(content={"results": ["Moscow", "Kazan"]})
    )

    weather_service = WeatherService(
        history_service=MagicMock(),
        city_service=MagicMock(),
        weather_client=mock_weather_client,
    )

    query = "M"
    result = await weather_service.autocomplete(query)

    mock_weather_client.autocomplete.assert_awaited_once_with(query=query)

    body_str = result.body.decode("utf-8")
    assert "results" in body_str
    assert "Moscow" in body_str
