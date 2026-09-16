from fastapi import APIRouter, Depends

from models.common_model import StandardResponse
from models.mission_model import CreateMissionRequest
from services.mission import create_mission_service
from services.auth_service import validate_token

router = APIRouter(
    prefix="/mission",
    dependencies=[Depends(validate_token)]
)

@router.post("/create_mission", dependencies=[Depends(validate_token)])
def create_mission(request: CreateMissionRequest) -> StandardResponse:
    return create_mission_service.main(request)
