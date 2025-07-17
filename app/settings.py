from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).parent

DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = False
    # echo: bool = True


class UrlSettings(BaseModel):
    protocol: str = "http"
    host: str = "localhost"
    port: str = "8000"
    api_v1_prefix: str = "/api/v1"


class WaetherApiSettings(BaseSettings):
    url: str = "https://api.weatherapi.com/v1"
    WEATHER_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=f"../.env", env_file_encoding="utf-8")


class Settings(BaseSettings):

    db: DbSettings = DbSettings()
    url: UrlSettings = UrlSettings()
    weather: WaetherApiSettings = WaetherApiSettings()


settings = Settings()
