"""Request schemas for task endpoints."""
from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.core.config import get_settings

settings = get_settings()
status_description = f"Status options: {', '.join(settings.status_values)}."


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=settings.title_max, examples=["Book flights"])
    description: str = Field("", max_length=settings.desc_max, examples=["Use company travel portal"])
    status: str | None = Field(None, description=status_description, examples=["todo"])
    deadline: date | None = Field(None, description="Deadline in ISO format", examples=["2025-12-31"])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Finish documentation",
                "description": "Write API usage guide",
                "status": "doing",
                "deadline": "2025-12-15",
            }
        }
    )


class TaskUpdateRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=settings.title_max)
    description: str | None = Field(None, max_length=settings.desc_max)
    status: str | None = Field(None, description=status_description, examples=["done"])
    deadline: date | None = Field(None, description="Updated deadline", examples=["2025-12-20"])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Finish documentation v2",
                "description": "Add API error codes",
                "status": "done",
                "deadline": "2025-12-10",
            }
        }
    )


class TaskStatusUpdateRequest(BaseModel):
    status: str = Field(..., description=status_description, examples=["doing"])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "doing",
            }
        }
    )
