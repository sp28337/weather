import pytest

from fastapi.responses import JSONResponse
from unittest.mock import AsyncMock, MagicMock

from app.api_v1.histories.schemas import HistorySchemaTest
from app.api_v1.weatherapi.service import WeatherService
from app.core.exceptions import WeatherNotFoundException
from fastapi.responses import HTMLResponse


@pytest.fixture
def mock_history_service():
    service = MagicMock()
    service.read_last_history = AsyncMock(return_value=None)
    service.create_history = AsyncMock()
    service.read_user_histories = AsyncMock(return_value=[])
    return service


@pytest.fixture
def mock_city_service():
    service = MagicMock()
    service.increase_requested_field = AsyncMock()
    service.read_cities = AsyncMock(return_value=[])
    return service


@pytest.fixture
def mock_weather_client():
    service = MagicMock()
    service.get_weather = AsyncMock()
    return service


@pytest.fixture
def weather_service(mock_history_service, mock_city_service, mock_weather_client):
    return WeatherService(
        history_service=mock_history_service,
        city_service=mock_city_service,
        weather_client=mock_weather_client,
    )


pytestmark = pytest.mark.asyncio


async def test_get_layout__no_city_and_no_user(weather_service):
    request = MagicMock()
    request.cookies.get.return_value = None

    response = await weather_service.get_layout(request=request, city=None)

    assert isinstance(response, HTMLResponse)
    assert response.template.name == "welcome.htm"


async def test_get_layout__no_city_no_history(weather_service, mock_history_service):
    request = MagicMock()
    request.cookies.get.return_value = "user123"
    mock_history_service.read_last_history.return_value = None

    response = await weather_service.get_layout(request=request, city=None)

    assert response.template.name == "welcome.htm"

    mock_history_service.read_last_history.assert_awaited_once_with(user_id="user123")


async def test_get_layout__no_city_no_history_delete_cookie(
    weather_service, mock_history_service
):
    request = MagicMock()
    request.cookies.get.return_value = "user123"
    mock_history_service.read_last_history.return_value = None

    mock_response = MagicMock()
    weather_service.welcome = AsyncMock(return_value=mock_response)

    response = await weather_service.get_layout(request=request, city=None)

    weather_service.welcome.assert_awaited_once_with(request=request)
    mock_response.delete_cookie.assert_called_once_with("user123")
    assert response == mock_response


async def test_get_layout__no_city_set_cookie(weather_service, mock_history_service):
    request = MagicMock()
    request.cookies.get.return_value = "user123"
    mock_history_service.read_last_history.return_value = HistorySchemaTest(
        user_id="aaa", city="Pattaya", timestamp="1994-10-19"
    )

    response = await weather_service.get_layout(request=request, city=None)

    assert response.template.name == "content.htm"
    assert response.raw_headers[2][0] == b"set-cookie"
    assert (
        response.raw_headers[2][1]
        == b"user_id=user123; Max-Age=3144960000; Path=/; SameSite=lax"
    )

    mock_history_service.read_last_history.assert_awaited_once_with(user_id="user123")


async def test_get_layout__no_user_id_set_cookie(weather_service, mock_history_service):
    request = MagicMock()
    request.cookies.get.return_value = None
    mock_history_service.read_last_history.return_value = HistorySchemaTest(
        user_id="aaa", city="Pattaya", timestamp="1994-10-19"
    )

    response = await weather_service.get_layout(request=request, city="Moscow")
    cookie_info = response.raw_headers[2][1].split(b"; ")

    assert response.template.name == "content.htm"
    assert response.raw_headers[2][0] == b"set-cookie"
    assert cookie_info[1] == b"Max-Age=3144960000"
    assert cookie_info[2] == b"Path=/"
    assert cookie_info[3] == b"SameSite=lax"


async def test_get_layout__success(
    weather_service,
    mock_history_service,
    mock_city_service,
    mock_weather_client,
):
    request = MagicMock()
    request.cookies.get.return_value = None

    city = "Moscow"
    day_fake_data = {
        "current": {
            "cloud": 27,
            "condition": {
                "code": 1003,
                "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
                "text": "Partly Cloudy",
            },
            "dewpoint_c": 22.3,
            "dewpoint_f": 72.2,
            "feelslike_c": 31.9,
            "feelslike_f": 89.4,
            "gust_kph": 6.8,
            "gust_mph": 4.2,
            "heatindex_c": 31.9,
            "heatindex_f": 89.4,
            "humidity": 69,
            "is_day": 1,
            "last_updated": "2025-07-27 14:30",
            "last_updated_epoch": 1753601400,
            "precip_in": 0.0,
            "precip_mm": 0.0,
            "pressure_in": 29.81,
            "pressure_mb": 1009.0,
            "temp_c": 28.6,
            "temp_f": 83.5,
            "uv": 9.0,
            "vis_km": 10.0,
            "vis_miles": 6.0,
            "wind_degree": 25,
            "wind_dir": "NNE",
            "wind_kph": 5.0,
            "wind_mph": 3.1,
            "windchill_c": 28.6,
            "windchill_f": 83.5,
        },
        "forecast": {
            "forecastday": [
                {
                    "astro": {
                        "is_moon_up": 0,
                        "is_sun_up": 0,
                        "moon_illumination": 6,
                        "moon_phase": "Waxing Crescent",
                        "moonrise": "08:28 AM",
                        "moonset": "08:49 PM",
                        "sunrise": "06:30 AM",
                        "sunset": "06:37 PM",
                    },
                    "date": "2025-07-27",
                    "date_epoch": 1753574400,
                    "day": {
                        "avghumidity": 69,
                        "avgtemp_c": 28.6,
                        "avgtemp_f": 83.4,
                        "avgvis_km": 9.9,
                        "avgvis_miles": 6.0,
                        "condition": {
                            "code": 1063,
                            "icon": "//cdn.weatherapi.com/weather/64x64/day/176.png",
                            "text": "Patchy rain " "nearby",
                        },
                        "daily_chance_of_rain": 88,
                        "daily_chance_of_snow": 0,
                        "daily_will_it_rain": 1,
                        "daily_will_it_snow": 0,
                        "maxtemp_c": 28.8,
                        "maxtemp_f": 83.8,
                        "maxwind_kph": 9.7,
                        "maxwind_mph": 6.0,
                        "mintemp_c": 28.0,
                        "mintemp_f": 82.4,
                        "totalprecip_in": 0.11,
                        "totalprecip_mm": 2.83,
                        "totalsnow_cm": 0.0,
                        "uv": 2.7,
                    },
                    "hour": [
                        {
                            "chance_of_rain": 0,
                            "chance_of_snow": 0,
                            "cloud": 12,
                            "condition": {
                                "code": 1000,
                                "icon": "//cdn.weatherapi.com/weather/64x64/night/113.png",
                                "text": "Clear ",
                            },
                            "dewpoint_c": 22.7,
                            "dewpoint_f": 72.8,
                            "feelslike_c": 32.2,
                            "feelslike_f": 90.0,
                            "gust_kph": 7.4,
                            "gust_mph": 4.6,
                            "heatindex_c": 32.2,
                            "heatindex_f": 90.0,
                            "humidity": 70,
                            "is_day": 0,
                            "precip_in": 0.0,
                            "precip_mm": 0.0,
                            "pressure_in": 29.86,
                            "pressure_mb": 1011.0,
                            "snow_cm": 0.0,
                            "temp_c": 28.7,
                            "temp_f": 83.7,
                            "time": "2025-07-27 00:00",
                            "time_epoch": 1753549200,
                            "uv": 0,
                            "vis_km": 10.0,
                            "vis_miles": 6.0,
                            "will_it_rain": 0,
                            "will_it_snow": 0,
                            "wind_degree": 238,
                            "wind_dir": "WSW",
                            "wind_kph": 5.4,
                            "wind_mph": 3.4,
                            "windchill_c": 28.7,
                            "windchill_f": 83.7,
                        },
                        {
                            "chance_of_rain": 0,
                            "chance_of_snow": 0,
                            "cloud": 15,
                            "condition": {
                                "code": 1000,
                                "icon": "//cdn.weatherapi.com/weather/64x64/night/113.png",
                                "text": "Clear ",
                            },
                            "dewpoint_c": 22.7,
                            "dewpoint_f": 72.8,
                            "feelslike_c": 32.2,
                            "feelslike_f": 90.0,
                            "gust_kph": 7.3,
                            "gust_mph": 4.6,
                            "heatindex_c": 32.2,
                            "heatindex_f": 90.0,
                            "humidity": 70,
                            "is_day": 0,
                            "precip_in": 0.0,
                            "precip_mm": 0.0,
                            "pressure_in": 29.85,
                            "pressure_mb": 1011.0,
                            "snow_cm": 0.0,
                            "temp_c": 28.7,
                            "temp_f": 83.7,
                            "time": "2025-07-27 01:00",
                            "time_epoch": 1753552800,
                            "uv": 0,
                            "vis_km": 10.0,
                            "vis_miles": 6.0,
                            "will_it_rain": 0,
                            "will_it_snow": 0,
                            "wind_degree": 256,
                            "wind_dir": "WSW",
                            "wind_kph": 5.4,
                            "wind_mph": 3.4,
                            "windchill_c": 28.7,
                            "windchill_f": 83.7,
                        },
                    ],
                }
            ]
        },
        "location": {
            "country": "Indonesia",
            "lat": -0.14,
            "localtime": "2025-07-27 14:44",
            "localtime_epoch": 1753602284,
            "lon": 98.186,
            "name": "Bali",
            "region": "North Sumatra",
            "tz_id": "Asia/Jakarta",
        },
    }
    weather_fake_data = {
        "current": {
            "cloud": 27,
            "condition": {
                "code": 1003,
                "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
                "text": "Partly Cloudy",
            },
            "dewpoint_c": 22.3,
            "dewpoint_f": 72.2,
            "feelslike_c": 31.9,
            "feelslike_f": 89.4,
            "gust_kph": 6.8,
            "gust_mph": 4.2,
            "heatindex_c": 31.9,
            "heatindex_f": 89.4,
            "humidity": 69,
            "is_day": 1,
            "last_updated": "2025-07-27 14:30",
            "last_updated_epoch": 1753601400,
            "precip_in": 0.0,
            "precip_mm": 0.0,
            "pressure_in": 29.81,
            "pressure_mb": 1009.0,
            "temp_c": 28.6,
            "temp_f": 83.5,
            "uv": 9.0,
            "vis_km": 10.0,
            "vis_miles": 6.0,
            "wind_degree": 25,
            "wind_dir": "NNE",
            "wind_kph": 5.0,
            "wind_mph": 3.1,
            "windchill_c": 28.6,
            "windchill_f": 83.5,
        },
        "forecast": {
            "forecastday": [
                {
                    "astro": {
                        "is_moon_up": 0,
                        "is_sun_up": 0,
                        "moon_illumination": 6,
                        "moon_phase": "Waxing Crescent",
                        "moonrise": "08:28 AM",
                        "moonset": "08:49 PM",
                        "sunrise": "06:30 AM",
                        "sunset": "06:37 PM",
                    },
                    "date": "2025-07-27",
                    "date_epoch": 1753574400,
                    "day": {
                        "avghumidity": 69,
                        "avgtemp_c": 28.6,
                        "avgtemp_f": 83.4,
                        "avgvis_km": 9.9,
                        "avgvis_miles": 6.0,
                        "condition": {
                            "code": 1063,
                            "icon": "//cdn.weatherapi.com/weather/64x64/day/176.png",
                            "text": "Patchy rain " "nearby",
                        },
                        "daily_chance_of_rain": 88,
                        "daily_chance_of_snow": 0,
                        "daily_will_it_rain": 1,
                        "daily_will_it_snow": 0,
                        "maxtemp_c": 28.8,
                        "maxtemp_f": 83.8,
                        "maxwind_kph": 9.7,
                        "maxwind_mph": 6.0,
                        "mintemp_c": 28.0,
                        "mintemp_f": 82.4,
                        "totalprecip_in": 0.11,
                        "totalprecip_mm": 2.83,
                        "totalsnow_cm": 0.0,
                        "uv": 2.7,
                    },
                },
                {
                    "astro": {
                        "is_moon_up": 0,
                        "is_sun_up": 1,
                        "moon_illumination": 11,
                        "moon_phase": "Waxing Crescent",
                        "moonrise": "09:12 AM",
                        "moonset": "09:32 PM",
                        "sunrise": "06:30 AM",
                        "sunset": "06:37 PM",
                    },
                    "date": "2025-08-02",
                    "date_epoch": 1754092800,
                    "day": {
                        "avghumidity": 79,
                        "avgtemp_c": 27.7,
                        "avgtemp_f": 81.8,
                        "avgvis_km": 10.0,
                        "avgvis_miles": 6.0,
                        "condition": {
                            "code": 1189,
                            "icon": "//cdn.weatherapi.com/weather/64x64/day/302.png",
                            "text": "Moderate rain",
                        },
                        "daily_chance_of_rain": 89,
                        "daily_chance_of_snow": 0,
                        "daily_will_it_rain": 1,
                        "daily_will_it_snow": 0,
                        "maxtemp_c": 27.9,
                        "maxtemp_f": 82.2,
                        "maxwind_kph": 33.5,
                        "maxwind_mph": 20.8,
                        "mintemp_c": 27.1,
                        "mintemp_f": 80.8,
                        "totalprecip_in": 0.35,
                        "totalprecip_mm": 8.83,
                        "totalsnow_cm": 0.0,
                        "uv": 7.0,
                    },
                },
            ]
        },
        "location": {
            "country": "Indonesia",
            "lat": -0.14,
            "localtime": "2025-07-27 14:41",
            "localtime_epoch": 1753602096,
            "lon": 98.186,
            "name": "Bali",
            "region": "North Sumatra",
            "tz_id": "Asia/Jakarta",
        },
    }

    mock_weather_client.side_effect = [
        day_fake_data,
        weather_fake_data,
    ]

    response = await weather_service.get_layout(request=request, city=city)

    mock_city_service.increase_requested_field.assert_awaited_once_with(city_name=city)
    mock_history_service.create_history.assert_awaited_once()
    mock_history_service.read_user_histories.assert_awaited_once()

    assert isinstance(response, HTMLResponse)
    assert response.template.name == "content.htm"


async def test_get_layout__not_found(weather_service, mock_weather_client):
    request = MagicMock()
    request.cookies.get.return_value = None
    city = "UnknownCity"

    mock_weather_client.get_weather.side_effect = WeatherNotFoundException()

    response = await weather_service.get_layout(request=request, city=city)

    mock_weather_client.get_weather.assert_awaited_once_with(city=city, days=2, tp=1)

    assert response.template.name == "not_found.htm"


@pytest.mark.asyncio
async def test_autocomplete__success():
    mock_weather_client = MagicMock()
    mock_weather_client.autocomplete = AsyncMock(
        return_value=JSONResponse(content={"results": ["Moscow", "Miami"]})
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
