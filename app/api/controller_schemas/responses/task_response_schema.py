"""Response schemas for task endpoints."""
from __future__ import annotations

from datetime import datetime, date

from pydantic import BaseModel, ConfigDict


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    deadline: date | None
    closed_at: datetime | None
    created_at: datetime
    updated_at: datetime
    project_id: str

    model_config = ConfigDict(from_attributes=True)

