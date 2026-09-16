from pydantic import BaseModel, Field, model_validator

from models.common_model import StrField, DecimalField


class ContributionPerPerson(BaseModel):
    pay_by: int
    pay_percentage: DecimalField

class ContributionToProject(BaseModel):
    contribute_to: int
    contribute_percentage: DecimalField

class CreateMissionRequest(BaseModel):
    title: str = StrField()
    pay: DecimalField
    pay_by: list[ContributionPerPerson] = Field(min_length=1)
    contribution: list[ContributionToProject] = Field(min_length=1)
    requires_audit: bool = True

    @model_validator(mode="after")
    def percentage_validator(self):
        if sum([contribution_item.contribute_percentage for contribution_item in self.contribution]) != DecimalField(100):
            raise ValueError("contribute_percentage values must total 100")

        if sum([pay_item.pay_percentage for pay_item in self.pay_by]) != DecimalField(100):
            raise ValueError("pay_percentage values must total 100")

        return self
