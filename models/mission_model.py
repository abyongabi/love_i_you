from pydantic import BaseModel

from models.common_model import StrField


class ContributionPerPerson(BaseModel):
    pay_by: int
    pay_percentage: int

class ContributionToProject(BaseModel):
    contribute_to: int
    contribute_percentage: int

class CreateMissionRequest(BaseModel):
    title: str = StrField()
    pay: float
    pay_by: list[ContributionPerPerson]
    contribution: list[ContributionToProject]
    requires_audit: bool = True
    
