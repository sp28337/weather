from pydantic import BaseModel


class Condition(BaseModel):
    code: int
    icon: str
    text: str


class CurrentWeather(BaseModel):
    cloud: int
    condition: Condition
    dewpoint_c: float
    dewpoint_f: float
    feelslike_c: float
    feelslike_f: float
    gust_kph: float
    gust_mph: float
    heatindex_c: float
    heatindex_f: float
    humidity: int
    is_day: int
    last_updated: str
    last_updated_epoch: int
    precip_in: float
    precip_mm: float
    pressure_in: float
    pressure_mb: float
    temp_c: float
    temp_f: float
    uv: float
    vis_km: float
    vis_miles: float
    wind_degree: int
    wind_dir: str
    wind_kph: float
    wind_mph: float
    windchill_c: float
    windchill_f: float


class Astro(BaseModel):
    is_moon_up: int
    is_sun_up: int
    moon_illumination: int
    moon_phase: str
    moonrise: str
    moonset: str
    sunrise: str
    sunset: str


class DayCondition(BaseModel):
    code: int
    icon: str
    text: str


class Day(BaseModel):
    avghumidity: int
    avgtemp_c: float
    avgtemp_f: float
    avgvis_km: float
    avgvis_miles: float
    condition: DayCondition
    daily_chance_of_rain: int
    daily_chance_of_snow: int
    daily_will_it_rain: int
    daily_will_it_snow: int
    maxtemp_c: float
    maxtemp_f: float
    maxwind_kph: float
    maxwind_mph: float
    mintemp_c: float
    mintemp_f: float
    totalprecip_in: float
    totalprecip_mm: float
    totalsnow_cm: float
    uv: float


class HourCondition(BaseModel):
    code: int
    icon: str
    text: str


class Hour(BaseModel):
    chance_of_rain: int
    chance_of_snow: int
    cloud: int
    condition: HourCondition
    dewpoint_c: float
    dewpoint_f: float
    feelslike_c: float
    feelslike_f: float
    gust_kph: float
    gust_mph: float
    heatindex_c: float
    heatindex_f: float
    humidity: int
    is_day: int
    precip_in: float
    precip_mm: float
    pressure_in: float
    pressure_mb: float
    snow_cm: float
    temp_c: float
    temp_f: float
    time: str
    time_epoch: int
    uv: float
    vis_km: float
    vis_miles: float
    will_it_rain: int
    will_it_snow: int
    wind_degree: int
    wind_dir: str
    wind_kph: float
    wind_mph: float
    windchill_c: float
    windchill_f: float


class ForecastDay(BaseModel):
    astro: Astro
    date: str
    date_epoch: int
    day: Day
    hour: list[Hour]


class Forecast(BaseModel):
    forecastday: list[ForecastDay]


class Location(BaseModel):
    country: str
    lat: float
    localtime: str
    localtime_epoch: int
    lon: float
    name: str
    region: str
    tz_id: str


class WeatherResponse(BaseModel):
    location: Location
    current: CurrentWeather
    forecast: Forecast
