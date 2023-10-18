from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


from typing import Tuple, Type

from pydantic import Field, PostgresDsn, SecretStr

class Config(BaseSettings):
    PG_DSN: PostgresDsn = Field(
        default = 'postgres://user:pass@localhost:5432/foobar',
    )

    jwt_secret: SecretStr = Field(
        alias='JWT_SECRET'
    )

    reset_password_token_secret: SecretStr = Field(
        alias='RESET_PASSWORD_TOKEN_SECRET'
    )

    verification_token_secret: SecretStr = Field(
        alias='VERIFICATION_TOKEN_SECRET'
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