from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models.common_model import StandardResponse
from models.user_model import LoginRequest
from services.user import login_service
from services.auth_service import decode_token


router = APIRouter(
    prefix="/auth"
)

optional_bearer = HTTPBearer(auto_error=False)

@router.get("/login")
def login(request: Annotated[LoginRequest, Query()]) -> StandardResponse:
    return login_service.main(request)
