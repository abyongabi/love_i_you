from typing import Annotated

from fastapi import APIRouter, Depends, Query

from models.common_model import StandardResponse
from models.user_model import CreateUserRequest, LoginRequest
from services.user import create_user_service, login_service
from services.auth_service import validate_token


router = APIRouter(
    prefix="/users",
    dependencies=[Depends(validate_token)]
)

@router.post("/create_user", dependencies=[Depends(validate_token)])
def create_user(request: CreateUserRequest) -> StandardResponse:
    return create_user_service.main(request)
