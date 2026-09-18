from datetime import datetime
from base import BaseModel
from pydantic import Field
from typing import Optional


class StrainProfile(BaseModel):
    id: int | None = None
    strain_id: int
    source_id: int
    description: str | None = None
    terpenes: list[str] = Field(
    default_factory=list
    )
    top_effects: list[str] = Field(
    default_factory=list
    )
    top_flavors: list[str] = Field(
    default_factory=list
    )
    cannabinoids: dict = {}
    create_at: Optional[datetime] = Field(alias="create_date")
