from typing import Tuple, Type, List

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from pydantic import Field, SecretStr, AmqpDsn

class Config(BaseSettings):

    RABBITMQ_DSN: AmqpDsn = Field(alias="RABBITMQ_DSN")
    TELEGRAM_BOT_TOKEN: SecretStr = Field(description="Telegram bot token registered through BotFather")
    TELEGRAM_USER_IDS: List = Field(alias="TELEGRAM_USER_IDS")
    EXCHANGE_NAME: str = Field(default="telegram_notify", description="ampq exchanger name")
    QUEUE_NAME: str = Field(default="simple_queue", description="ampq exchanger queue name")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return dotenv_settings, env_settings, init_settings

def load_config(*arg, **vararg) -> Config:
    return Config(*arg, **vararg)