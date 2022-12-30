from typing import Optional

import requests
from fastapi import APIRouter, Response, Request, Depends
from sqlalchemy.orm import Session

from app.common import consts
from app.core.settings.setting import AppSettings, get_env
from app.models.common import SnsType, AuthorizationCode
from app.database.conn import db
from app.models.users import User
from app.services.jwt import create_access_token
from app.services.authentication import getUserProfile, createKakaoUser, readKakaoUserRow

router = APIRouter()


@router.post('/{sns_type}/auth')
async def loginCallback(
        sns_type: SnsType,
        auth: AuthorizationCode,
        response: Response,
        request: Request,
        const: AppSettings = Depends(get_env),
        session: Session = Depends(db.session),
) -> dict[str: str]:
    print("======================= Kakao loginCallback =======================")
    if sns_type == SnsType.kakao:
        # kakaoAuthURL = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={consts.KAKAO_CLIENT_ID}&code={auth.code}&redirect_uri={consts.KAKAO_REDIRECT_URI}&client_secret={consts.KAKAO_CLIENT_SECRET}"
        kakaoAuthURL = f"https://kauth.kakao.com/oauth/token?" \
                       f"grant_type=authorization_code&" \
                       f"client_id={const.kakao_client_id}&" \
                       f"code={auth.code}&" \
                       f"redirect_uri={const.kakao_redirect_client_uri}&" \
                       f"client_secret={str(const.kakao_client_secret.get_secret_value())}"
        user_code = requests.post(kakaoAuthURL).json()
        print(user_code)
        refresh_token = user_code.get('refresh_token')
        user_profile = getUserProfile(user_code.get('access_token'))
        user_id = user_profile.get('id')
        user_nickname = user_profile.get('properties').get('nickname')
        user_row = readKakaoUserRow(user_id)
        if user_row is None:
            createKakaoUser(user_profile, session)
        user = User(user_id=user_id, nickname=user_nickname)
        access_token = create_access_token(user)
        response.set_cookie(key='token', value=access_token, httponly=True)
        response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)
    return dict(userID=user_id, nickName=user_nickname)

    # return {'result': True}


# @router.get('/{sns_type}/logout')
# async def logout(request: Request, response: Response, sns_type: SnsType):
#     if sns_type == SnsType.kakao:
#         print("======================= Kakao logout =======================")
#         url = "https://kapi.kakao.com/v1/user/logout"
#         # KEY = request.cookies.get('kakao')
#         KEY = request.cookies.get(f'{sns_type}')
#         headers = dict(Authorization=f"Bearer {KEY}")
#         res = requests.post(url, headers=headers)
#         response.set_cookie(key=f'{SnsType.kakao}', value=None)
#         return logoutReturnTemp(res.json())
#         # return {"logout": res.json()}
#     print("not in")
#     return {"logout": "failed"}


# @router.get('/{sns_type}/unlink')
# async def unlink(request: Request, response: Response, sns_type: SnsType):
#     if sns_type == SnsType.kakao:
#         print("In Kakao")
#         url = "https://kapi.kakao.com/v1/user/unlink"
#         KEY = request.cookies.get('kakao')
#         headers = dict(Authorization=f"Bearer {KEY}")
#         res = requests.post(url, headers=headers)
#         response.set_cookie(key=SnsType.kakao, value=None)
#         return unlinkReturnTemp(res)
#         # return {"logout": res.json()}
#     print("not in")
#     return {"logout": "failed"}


# @app.get('/kakaoLogout')
# def kakaoLogout(request: Request, response: Response):
#     url = "https://kapi.kakao.com/v1/user/unlink"
#     KEY = request.cookies['kakao']
#     headers = dict(Authorization=f"Bearer {KEY}")
#     _res = requests.post(url,headers=headers)
#     response.set_cookie(key="kakao", value=None)
#     return {"logout": _res.json()}
