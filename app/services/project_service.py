"""Business logic for projects."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.models import Project
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services import exceptions as exc


class ProjectService:
    def __init__(self, session: Session, settings: Settings | None = None):
        self.session = session
        self.settings = settings or get_settings()
        self.project_repo = ProjectRepository(session)
        self.task_repo = TaskRepository(session)

    def list_projects(self) -> list[Project]:
        return list(self.project_repo.list_projects())

    def get_project(self, project_id: str) -> Project:
        project = self.project_repo.get(project_id)
        if not project:
            raise exc.NotFoundError("Project not found.")
        return project

    def create_project(self, name: str, description: str = "") -> Project:
        name = name.strip()
        description = description.strip()
        if not name:
            raise exc.ValidationError("Project name cannot be empty.")
        if len(name) > self.settings.title_max:
            raise exc.ValidationError(f"Project name cannot exceed {self.settings.title_max} characters.")
        if len(description) > self.settings.desc_max:
            raise exc.ValidationError(f"Project description cannot exceed {self.settings.desc_max} characters.")
        if self.project_repo.count() >= self.settings.max_projects:
            raise exc.ConflictError("Maximum number of projects reached.")
        if self.project_repo.get_by_name(name):
            raise exc.ConflictError("Project name already exists.")

        project = Project(name=name, description=description)
        return self.project_repo.add(project)

    def update_project(self, project_id: str, name: str | None = None, description: str | None = None) -> Project:
        project = self.get_project(project_id)
        if name is not None:
            cleaned_name = name.strip()
            if not cleaned_name:
                raise exc.ValidationError("Project name cannot be empty.")
            if len(cleaned_name) > self.settings.title_max:
                raise exc.ValidationError(f"Project name cannot exceed {self.settings.title_max} characters.")
            existing = self.project_repo.get_by_name(cleaned_name)
            if existing and existing.id != project.id:
                raise exc.ConflictError("Project name already exists.")
            project.name = cleaned_name

        if description is not None:
            cleaned_desc = description.strip()
            if len(cleaned_desc) > self.settings.desc_max:
                raise exc.ValidationError(f"Project description cannot exceed {self.settings.desc_max} characters.")
            project.description = cleaned_desc

        return project

    def delete_project(self, project_id: str) -> None:
        project = self.get_project(project_id)
        self.project_repo.delete(project)

    def count_all_tasks(self) -> int:
        return self.task_repo.count_all()

