from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv


class Settings(BaseSettings):
    app_name: str = 'Line-Provider'
    debug: bool
    line_provider_host: str
    line_provider_port: int

    # RabbitMQ
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "user"
    rabbitmq_password: str = "password"
    rabbitmq_queue: str = "event_updates"

    model_config = SettingsConfigDict(env_file=find_dotenv(), case_sensitive=False, extra="allow")


settings = Settings()
