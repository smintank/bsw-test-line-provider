from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Общие настройки
    app_name: str = "Bet Maker"
    debug: bool = False
    is_single: bool = True

    # PostgreSQL
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    # Сервисы
    bet_maker_host: str
    bet_maker_port: int
    line_provider_host: str
    line_provider_port: int

    # RabbitMQ
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "user"
    rabbitmq_password: str = "password"
    rabbitmq_queue: str = "event_updates"

    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        case_sensitive=False,
        extra="allow"
    )

    @property
    def event_app_url(self) -> str:
        return f"http://{self.line_provider_host}:{self.line_provider_port}/events/"


settings = Settings()
