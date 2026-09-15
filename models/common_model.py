from typing import Annotated

from pydantic import Field, BaseModel


StrField = Annotated[str, Field(min_length=10, max_length=100)]


class StandardResponse(BaseModel):
    success: bool
    message: str | None = ""
