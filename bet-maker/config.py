
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    postgres_url: str
    debug: bool
    events_url: str | None = None
    is_single: bool = True

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
