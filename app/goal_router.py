from fastapi import APIRouter, Depends

from models.common_model import StandardResponse
from models.goal_model import CreateGoalRequest
from services.goal import create_goal_service
from services.auth_service import validate_token

router = APIRouter(
    prefix="/goal",
    dependencies=[Depends(validate_token)]
)

@router.post("/create_goal", dependencies=[Depends(validate_token)])
def create_goal(request: CreateGoalRequest) -> StandardResponse:
    return create_goal_service.main(request)
