"""FastAPI entrypoint for the ToDoList Web API (Phase 3)."""
from fastapi import FastAPI

from app.api.routers import api_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="ToDoList API",
        version="1.0.0",
        description="RESTful API for managing projects and tasks.",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
    )
    app.state.settings = settings
    app.include_router(api_router)
    return app


app = create_app()
