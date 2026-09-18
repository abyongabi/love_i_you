from fastapi import APIRouter, Depends

from models.common_model import StandardResponse
from models.goal_model import CreateGoalRequest, UpdateGoalRequest
from services.goal import create_goal_service, get_goal_service, update_goal_service
from services.auth_service import validate_token

router = APIRouter(
    prefix="/goal",
    dependencies=[Depends(validate_token)]
)

@router.post("/create_goal")
def create_goal(request: CreateGoalRequest) -> StandardResponse:
    return create_goal_service.main(request)


@router.get("/get_goal")
def get_goal(room_id: int | None = None, goal_id: int | None = None):
    return get_goal_service.main(room_id, goal_id)


@router.post("/update_goal")
def update_goal(request: UpdateGoalRequest) -> StandardResponse:
    return update_goal_service.main(request)
