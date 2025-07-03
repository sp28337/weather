from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    WEATHER_API_KEY: str = ""
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = True

    model_config = SettingsConfigDict(env_file=f"../.env", env_file_encoding="utf-8")
