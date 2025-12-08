"""Request schemas for project endpoints."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.core.config import get_settings

settings = get_settings()


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=settings.title_max, examples=["Personal board"])
    description: str = Field(
        default="",
        max_length=settings.desc_max,
        description="Optional project description.",
        examples=["Things I must do before travel"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Sprint Planning",
                "description": "Stories and tasks for the sprint.",
            }
        }
    )


class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=settings.title_max)
    description: str | None = Field(None, max_length=settings.desc_max)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated project name",
                "description": "Refined scope and notes.",
            }
        }
    )

