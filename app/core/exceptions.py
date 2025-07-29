class CityNotFoundException(Exception):
    detail = "City not found"


class HistoryNotFoundException(Exception):
    detail = "History not found"


class HistoryCreateFailException(Exception):
    detail = "Incorrect new history data"


class WeatherNotFoundException(Exception):
    detail = "Weather not found"
