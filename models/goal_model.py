from pydantic import BaseModel, Field

from models.common_model import StrField, IntField


class CreateGoalRequest(BaseModel):
    title: str = StrField()
    budget: float = 1
    room_id: int | None = None
    priority: int = Field(ge=1, default=1)


class UpdateGoalRequest(CreateGoalRequest):
    goal_id: int = IntField()
    active: bool = True
