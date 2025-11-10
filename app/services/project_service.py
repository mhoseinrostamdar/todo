from typing import List, Optional
from app.models import ProjectORM
from app.repositories import ProjectRepository
from app.exceptions import ValidationError, NotFoundError
import os
from dotenv import load_dotenv

load_dotenv()

MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT", 50))
TITLE_MAX = int(os.getenv("TITLE_MAX", 30))
DESC_MAX = int(os.getenv("DESC_MAX", 150))


class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    def create_project(self, name: str, description: str = "") -> ProjectORM:
        name = name.strip()
        if not name:
            raise ValidationError("Project name cannot be empty.")
        if len(name) > TITLE_MAX:
            raise ValidationError(f"Project name length cannot exceed {TITLE_MAX}.")
        if self.project_repo.get_by_name(name):
            raise ValidationError("Project name already exists.")
        if len(self.project_repo.get_all()) >= MAX_NUMBER_OF_PROJECT:
            raise ValidationError("Maximum number of projects reached.")
        project = ProjectORM(name=name, description=description.strip())
        return self.project_repo.add(project)

    def get_project(self, project_id: str) -> ProjectORM:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found.")
        return project

    def update_project(self, project_id: str, name: Optional[str] = None, description: Optional[str] = None) -> ProjectORM:
        project = self.get_project(project_id)
        if name:
            if len(name) > TITLE_MAX:
                raise ValidationError(f"Project name length cannot exceed {TITLE_MAX}.")
            if name != project.name and self.project_repo.get_by_name(name):
                raise ValidationError("New project name already exists.")
            project.name = name
        if description is not None:
            if len(description) > DESC_MAX:
                raise ValidationError(f"Description length cannot exceed {DESC_MAX}.")
            project.description = description
        return self.project_repo.update(project)

    def delete_project(self, project_id: str) -> None:
        project = self.get_project(project_id)
        self.project_repo.delete(project)

    def list_projects(self) -> List[ProjectORM]:
        return self.project_repo.get_all()
