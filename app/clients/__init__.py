from .city import (
    create_city_client,
    update_city_partial_client,
    get_city_by_name_client,
    get_cities_client,
)
from .history import (
    create_history_client,
    get_last_history_client,
)
from .weather import (
    get_weather_client,
    autocomplete_client,
)


__all__ = [
    "create_city_client",
    "update_city_partial_client",
    "get_city_by_name_client",
    "get_cities_client",
    "create_history_client",
    "get_last_history_client",
    "get_weather_client",
    "autocomplete_client",
]
