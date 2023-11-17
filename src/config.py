from typing import List, Type
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        extra = "allow"


class DevConfig(Settings):
    CONFIG_NAME: str = "dev"


class ProdConfig(Settings):
    CONFIG_NAME: str = "prod"


def get_config(config):
    return config_by_name[config]


EXPORT_CONFIGS: List[Type[Settings]] = [
    DevConfig,
    ProdConfig,
]
config_by_name = {cfg().CONFIG_NAME: cfg() for cfg in EXPORT_CONFIGS}
