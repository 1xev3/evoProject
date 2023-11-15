from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


from typing import Tuple, Type

from pydantic import Field, PostgresDsn, AmqpDsn

class Config(BaseSettings):
    pg_dsn: PostgresDsn = Field(
        default = 'postgres://user:pass@localhost:5432/foobar',
    )
    
    RABBITMQ_DSN: AmqpDsn = Field(description="Ampq dsn for RabbitMQ")
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