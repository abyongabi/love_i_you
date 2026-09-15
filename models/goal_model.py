from pydantic import BaseModel

from models.common_model import StrField


class CreateGoalRequest(BaseModel):
    title: str = StrField()
    budget: float
