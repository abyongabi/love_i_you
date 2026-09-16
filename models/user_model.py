from pydantic import BaseModel

from models.common_model import StrField, IntField


class CreateUserRequest(BaseModel):
    username: str = StrField()
    password: str = StrField()
    email: str = StrField()


class LoginRequest(BaseModel):
    username: str = StrField()
    password: str = StrField()


class CreateRoomRequest(BaseModel):
    roomname: str = StrField()


class CreateUpdateUserAccessRequest(BaseModel):
    user_id: int = IntField()
    room_access: list[IntField]
