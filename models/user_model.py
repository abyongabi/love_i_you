from pydantic import BaseModel

from models.common_model import StrField


class CreateUserRequest(BaseModel):
    username: str = StrField()
    password: str = StrField()
    email: str = StrField()


class LoginRequest(BaseModel):
    username: str = StrField()
    password: str = StrField()
