from functools import lru_cache

from pydantic import SecretStr

from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    version: str = "0.1.0"
    app_env: str

    db_user: str
    db_password: SecretStr
    db_host: str
    db_schema: str

    kakao_client_id: str
    kakao_client_secret: SecretStr
    kakao_redirect_client_uri: str
    kakao_redirect_server_uri: str
    kakao_iss_url: str

    jwt_secret_key: SecretStr
    jwt_algorithm: str

    class Config:
        validate_assignment = True


@lru_cache
def get_env() -> AppSettings:
    return AppSettings()

