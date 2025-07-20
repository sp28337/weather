class CityNotFoundException(Exception):
    detail = "City not found"


class HistoryNotFoundException(Exception):
    detail = "History not found"


class WeatherNotFoundException(Exception):
    detail = "Weather not found"
