from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


from typing import Tuple, Type

from pydantic import Field, PostgresDsn

class Config(BaseSettings):
    pg_dsn: PostgresDsn = Field(
        default = 'postgres://user:pass@localhost:5432/foobar',
    )

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