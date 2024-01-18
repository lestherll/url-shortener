from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cache_dsn: str = "127.0.0.1:11211"
    db_dsn: str = "sqlite+aiosqlite:///:memory:"
    test_db_dsn: str = "sqlite+aiosqlite:///:memory:"
    model_config = SettingsConfigDict(env_file=".env", validate_default=True)


SETTINGS = Settings()
