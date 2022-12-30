from pydantic import BaseModel, dataclasses


class User(BaseModel):
    user_id: int
    nickname: str
    email: str = None
    profile_img: str = None

    # def __init__(self, user_id: int, nickname: str):
    #     self.nickname = nickname
    #     self.user_id = user_id
    #     self.email = None
    #     self.profile_img = None

    # @property
    # def email(self):
    #     return self.email
    #
    # @email.setter
    # def email(self, email):
    #     self.email = email
    #
    # @property
    # def profile_img(self):
    #     return self.profile_img
    #
    # @profile_img.setter
    # def profile_img(self, profile_img):
    #     self.profile_img = profile_img
