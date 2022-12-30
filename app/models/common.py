from enum import Enum
from pydantic import BaseModel


class Feeling(int, Enum):
    Happiness: int = 1
    Sadness: int = 2
    Boring: int = 3


class Reaction(int, Enum):
    Like: int = 1
    Hate: int = 2


class SnsType(str, Enum):
    kakao: str = "kakao"
    google: str = "google"


class AuthorizationCode(BaseModel):
    code: str
