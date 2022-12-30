from typing import Dict, Optional

import requests
from sqlalchemy.orm import Session

from app.database.schema import Users


def getUserProfile(access_token: str):
    return requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()


def createKakaoUser(data: Dict, session: Session) -> None:
    Users.create(
        session,
        auto_commit=True,
        uid=data.get('id'),
        name=data.get('properties').get('nickname'),
        profile_img=data.get('properties').get('profile_image'),
        email=data.get('kakao_account').get('email'),
        gender=data.get('kakao_account').get('gender'),
        birth=data.get('kakao_account').get('birthday')
    )


def readKakaoUserRow(uid: str) -> Optional:
    row = Users.get(uid=uid)
    return row
