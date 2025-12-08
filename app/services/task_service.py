"""Business logic for tasks."""
from __future__ import annotations

from datetime import datetime, date

from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.models import Task
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services import exceptions as exc


class TaskService:
    def __init__(self, session: Session, settings: Settings | None = None):
        self.session = session
        self.settings = settings or get_settings()
        self.project_repo = ProjectRepository(session)
        self.task_repo = TaskRepository(session)

    def list_tasks(self, project_id: str) -> list[Task]:
        self._ensure_project_exists(project_id)
        return list(self.task_repo.list_for_project(project_id))

    def get_task(self, project_id: str, task_id: str) -> Task:
        self._ensure_project_exists(project_id)
        task = self.task_repo.get(task_id)
        if not task or task.project_id != project_id:
            raise exc.NotFoundError("Task not found.")
        return task

    def create_task(
        self,
        project_id: str,
        title: str,
        description: str = "",
        status: str | None = None,
        deadline: date | None = None,
    ) -> Task:
        project = self._ensure_project_exists(project_id)
        title = title.strip()
        description = description.strip()
        if not title:
            raise exc.ValidationError("Task title cannot be empty.")
        if len(title) > self.settings.title_max:
            raise exc.ValidationError(f"Task title cannot exceed {self.settings.title_max} characters.")
        if len(description) > self.settings.desc_max:
            raise exc.ValidationError(f"Task description cannot exceed {self.settings.desc_max} characters.")
        if self.task_repo.count_all() >= self.settings.max_tasks:
            raise exc.ConflictError("Maximum number of tasks reached.")

        resolved_status = status or "todo"
        self._validate_status(resolved_status)

        task = Task(
            title=title,
            description=description,
            status=resolved_status,
            deadline=deadline,
            project_id=project.id,
        )
        self._set_closed_at(task, resolved_status)
        return self.task_repo.add(task)

    def update_task(
        self,
        project_id: str,
        task_id: str,
        title: str | None = None,
        description: str | None = None,
        status: str | None = None,
        deadline: date | None = None,
    ) -> Task:
        task = self.get_task(project_id, task_id)

        if title is not None:
            cleaned = title.strip()
            if not cleaned:
                raise exc.ValidationError("Task title cannot be empty.")
            if len(cleaned) > self.settings.title_max:
                raise exc.ValidationError(f"Task title cannot exceed {self.settings.title_max} characters.")
            task.title = cleaned

        if description is not None:
            cleaned_desc = description.strip()
            if len(cleaned_desc) > self.settings.desc_max:
                raise exc.ValidationError(f"Task description cannot exceed {self.settings.desc_max} characters.")
            task.description = cleaned_desc

        if status is not None:
            self._validate_status(status)
            task.status = status
            self._set_closed_at(task, status)

        if deadline is not None:
            task.deadline = deadline
            if status == "done":
                self._set_closed_at(task, status)

        task.updated_at = datetime.utcnow()
        return task

    def change_status(self, project_id: str, task_id: str, status: str) -> Task:
        task = self.get_task(project_id, task_id)
        self._validate_status(status)
        task.status = status
        self._set_closed_at(task, status)
        task.updated_at = datetime.utcnow()
        return task

    def delete_task(self, project_id: str, task_id: str) -> None:
        task = self.get_task(project_id, task_id)
        self.task_repo.delete(task)

    def _validate_status(self, status: str) -> None:
        if status not in self.settings.status_values:
            allowed = ", ".join(self.settings.status_values)
            raise exc.ValidationError(f"Status must be one of: {allowed}.")

    def _ensure_project_exists(self, project_id: str):
        project = self.project_repo.get(project_id)
        if not project:
            raise exc.NotFoundError("Project not found.")
        return project

    @staticmethod
    def _set_closed_at(task: Task, status: str) -> None:
        if status == "done":
            task.closed_at = datetime.utcnow()
        else:
            task.closed_at = None
