from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    debug: bool
    bet_maker_host: str
    bet_maker_port: int
    events_url: str | None = None
    is_single: bool = True

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="allow")


settings = Settings()
