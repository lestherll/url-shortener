from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cache_dsn: str = "127.0.0.1:11211"
    model_config = SettingsConfigDict(env_file=".env", validate_default=True)


SETTINGS = Settings()
