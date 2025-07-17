from app.clients.city import (
    create_city_client,
    update_city_partial_client,
    get_city_by_name_client,
    get_cities_client,
)
from app.clients.history import (
    create_history_client,
    get_last_history_client,
    get_histories_client,
)
from app.clients.weather import (
    get_weather_client,
    autocomplete_client,
)


__all__ = [
    "create_city_client",
    "update_city_partial_client",
    "get_city_by_name_client",
    "get_cities_client",
    "create_history_client",
    "get_histories_client",
    "get_last_history_client",
    "get_weather_client",
    "autocomplete_client",
]
