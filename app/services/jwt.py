from datetime import datetime, timedelta

import jwt
from fastapi import Depends

from app.common import consts
from app.core.settings.setting import AppSettings, get_env
from app.models.users import User


def create_access_token(
        user: User,
        env_const: AppSettings = get_env()
) -> dict[str: str]:
    return jwt.encode(
        payload=create_jwt_payload(user.user_id, user.nickname),
        key=str(env_const.jwt_secret_key.get_secret_value()),
        algorithm=env_const.jwt_algorithm
    )


def create_jwt_payload(
        user_id: str,
        nickname: str,
        env_const: AppSettings = get_env()
):
    return dict(
        iss=env_const.kakao_iss_url,
        aud=env_const.kakao_client_id,
        exp=datetime.utcnow() + timedelta(minutes=consts.ACCESS_TOKEN_EXPIRE_MINUTES),
        id=user_id,
        nickname=nickname
    )


# def verificationJWT(token: str, sys_type: SnsType) -> bool:
#     try:
#         if sys_type == SnsType.kakao:
#             jwt.decode(token, consts.JWT_SECRET_KEY, consts.JWT_ALGORITHM)
#     except jwt.ExpiredSignatureError as e:
#         print('\n', e)
#         return status.HTTP_401_UNAUTHORIZED
#     except jwt.InvalidTokenError as e:
#         print('\n', e)
#         return status.HTTP_401_UNAUTOHRIZED
#     else:
#         return True
