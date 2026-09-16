from decimal import Decimal
from typing import Annotated

from pydantic import Field, BaseModel


StrField = Annotated[str, Field(min_length=10, max_length=100)]

DecimalField = Annotated[Decimal, Field(ge=0, le=100)]

IntField = Annotated[int, Field(ge=1)]


class StandardResponse(BaseModel):
    success: bool
    message: str | None = ""
