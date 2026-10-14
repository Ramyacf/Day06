
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CaseCreate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = None


class CaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    created_by: UUID
    reference_code: str
    title: str | None
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime
