class CityNotFoundException(Exception):
    detail = "City not found"


class WeatherNotFoundException(Exception):
    detail = "Weather not found"
