from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from typing import Tuple, Type

from pydantic import Field, MongoDsn

class Config(BaseSettings):
    mongo_dsn: MongoDsn = Field(
        title="Mongo connection url",
        examples = ['mongodb://user:pass@localhost:27017/tech-support'],
    )
    minio_dsn: str = Field(
        title="Minio connection url",
        default="localhost:9000",
        examples=["0.0.0.0:9000"]
    )
    minio_access_key: str = Field(
        title="Minio access key (LOGIN)",
    )
    minio_secret_key: str = Field(
        title="Minio secret key (PASSWORD)",
    )
    minio_bucket_name: str = Field (
        title="Minio bucket to store images",
        default="product-service"
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