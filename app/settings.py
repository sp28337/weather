from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).parent

DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = False


class Settings(BaseSettings):
    WEATHER_API_KEY: str = ""
    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()

    model_config = SettingsConfigDict(env_file=f"../.env", env_file_encoding="utf-8")


settings = Settings()
