from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./nav_station.db"
    jwt_secret: str = "change-this-secret-in-production"
    jwt_expire_minutes: int = 60 * 24 * 7
    cors_origins: str = "https://nav.5ai.icu,http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
