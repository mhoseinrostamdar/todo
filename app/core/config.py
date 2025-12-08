"""Application configuration and shared settings."""
from __future__ import annotations

import os
from functools import lru_cache
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field, field_validator

load_dotenv()


class Settings(BaseModel):
    database_url: str = Field(..., alias="DATABASE_URL", description="SQLAlchemy database URL.")
    max_projects: int = Field(50, ge=1, alias="MAX_NUMBER_OF_PROJECT")
    max_tasks: int = Field(1000, ge=1, alias="MAX_NUMBER_OF_TASK")
    title_max: int = Field(30, ge=1, alias="TITLE_MAX")
    desc_max: int = Field(150, ge=1, alias="DESC_MAX")
    status_values: List[str] = Field(default_factory=lambda: ["todo", "doing", "done"], alias="STATUS_VALUES")

    @field_validator("status_values", mode="before")
    @classmethod
    def split_statuses(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        return [item.strip() for item in value.split(",") if item.strip()]

    model_config = ConfigDict(
        populate_by_name=True,
        frozen=True,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load settings from environment once."""
    return Settings(
        DATABASE_URL=os.getenv("DATABASE_URL", ""),
        MAX_NUMBER_OF_PROJECT=int(os.getenv("MAX_NUMBER_OF_PROJECT", "50")),
        MAX_NUMBER_OF_TASK=int(os.getenv("MAX_NUMBER_OF_TASK", "1000")),
        TITLE_MAX=int(os.getenv("TITLE_MAX", "30")),
        DESC_MAX=int(os.getenv("DESC_MAX", "150")),
        STATUS_VALUES=os.getenv("STATUS_VALUES", "todo,doing,done"),
    )
