"""FastAPI entrypoint for the ToDoList Web API (Phase 3)."""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

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
    # Helpful root endpoint to point users to documentation.
    @app.get("/", tags=["Meta"])
    def root():
        return {
            "status": "ok",
            "message": "ToDoList API",
            "docs": "/api/v1/docs",
            "openapi": "/api/v1/openapi.json",
        }

    @app.get("/docs", include_in_schema=False)
    def docs_redirect():
        return RedirectResponse(url="/api/v1/docs")

    app.include_router(api_router)
    return app


app = create_app()
