from dataclasses import dataclass
from os import path, environ

from app.core.settings.setting import AppSettings, get_env

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
    BASE_DIR = base_dir

    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True


@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True

    DB_USER: str = None
    DB_PASSWORD: str = None
    DB_HOST: str = None
    DB_SCHEMA: str = None
    DB_CHARSET: str = "utf8mb4"

    def __init__(self, env_const: AppSettings = get_env()):
        self.DB_USER = env_const.db_user
        self.DB_PASSWORD = str(env_const.db_password.get_secret_value())
        self.DB_HOST = env_const.db_host
        self.DB_SCHEMA = env_const.db_schema


@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = False


def conf():
    config = dict(prod=ProdConfig, local=LocalConfig)
    return config[environ.get('API_ENV', 'local')]()
