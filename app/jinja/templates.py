from pathlib import Path
from fastapi.templating import Jinja2Templates

from .filters import (
    weekday_short,
    weather_svg,
    moonset_filter,
    set_time,
    datetime_filter,
    get_next_hours,
    format_datetime,
)

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=TEMPLATES_DIR)
templates.env.filters["weekday_short"] = weekday_short
templates.env.filters["weather_svg"] = weather_svg
templates.env.filters["time_converter"] = moonset_filter
templates.env.filters["set_time"] = set_time
templates.env.filters["datetime_filter"] = datetime_filter
templates.env.filters["get_next_hours"] = get_next_hours
templates.env.filters["format_datetime"] = format_datetime
