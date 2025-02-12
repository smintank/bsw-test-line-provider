from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv


class Settings(BaseSettings):
    app_name: str = 'Bet Maker'
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    debug: bool
    bet_maker_host: str
    bet_maker_port: int
    line_provider_port: int
    line_provider_url: str = 'http://line-provider:{}/events/'
    is_single: bool = True

    model_config = SettingsConfigDict(env_file=find_dotenv(), case_sensitive=False, extra="allow")


settings = Settings()
