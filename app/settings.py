from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    WEATHER_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=f"../.env",
        env_file_encoding="utf-8"
    )
