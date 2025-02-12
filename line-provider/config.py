from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv


class Settings(BaseSettings):
    app_name: str = 'Line-Provider'
    debug: bool
    line_provider_host: str
    line_provider_port: int

    model_config = SettingsConfigDict(env_file=find_dotenv(), case_sensitive=False, extra="allow")


settings = Settings()
