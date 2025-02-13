from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv


class Settings(BaseSettings):

    app_name: str = "Bet Maker"

    # PostgreSQL
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    # Общие настройки
    debug: bool = False
    is_single: bool = True

    # Сервисы
    bet_maker_host: str
    bet_maker_port: int
    line_provider_host: str
    line_provider_port: int

    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        case_sensitive=False,
        extra="allow"
    )

    @property
    def event_app_url(self) -> str:
        return f"http://{self.line_provider_host}:{self.line_provider_port}/events/"


settings = Settings()
