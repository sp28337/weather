from fastapi.templating import Jinja2Templates
from app.utils.filters import (
    weekday_short,
    weather_svg,
    time_converter,
    set_time,
    datetime_filter,
    get_next_hours,
)

templates = Jinja2Templates(directory="templates")
templates.env.filters["weekday_short"] = weekday_short
templates.env.filters["weather_svg"] = weather_svg
templates.env.filters["time_converter"] = time_converter
templates.env.filters["set_time"] = set_time
templates.env.filters["datetime_filter"] = datetime_filter
templates.env.filters["get_next_hours"] = get_next_hours
