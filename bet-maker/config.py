
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_url: str
    debug: bool

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
