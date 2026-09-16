from fastapi import APIRouter, Depends

from models.common_model import StandardResponse
from models.user_model import CreateUserRequest, CreateRoomRequest, CreateUpdateUserAccessRequest
from services.user import create_user_service, create_room_service, get_room_service, create_update_user_access_service, get_user_service
from services.auth_service import validate_token


router = APIRouter(
    prefix="/users",
    dependencies=[Depends(validate_token)]
)

@router.post("/create_user")
def create_user(request: CreateUserRequest) -> StandardResponse:
    return create_user_service.main(request)


@router.post("/create_room")
def create_room(request: CreateRoomRequest) -> StandardResponse:
    return create_room_service.main(request)


@router.get("/get_room")
def get_room(request: int | None = None):
    return get_room_service.main(request)


@router.post("/create_update_user_access")
def create_update_user_access(request: CreateUpdateUserAccessRequest) -> StandardResponse:
    return create_update_user_access_service.main()


@router.get("/get_user")
def get_user(request: int) -> list:
    # This should be substitue with a more sophsiticate response ideally the response can be used to contruct the token
    return get_user_service.main(request)