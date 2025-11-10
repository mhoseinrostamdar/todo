from typing import List, Optional
from datetime import datetime, date
from app.models import TaskORM, ProjectORM
from app.repositories import TaskRepository, ProjectRepository
from app.exceptions import ValidationError, NotFoundError
import os
from dotenv import load_dotenv

load_dotenv()

MAX_NUMBER_OF_TASK = int(os.getenv("MAX_NUMBER_OF_TASK", 1000))
TITLE_MAX = int(os.getenv("TITLE_MAX", 30))
DESC_MAX = int(os.getenv("DESC_MAX", 150))
STATUS_VALUES = os.getenv("STATUS_VALUES", "todo,doing,done").split(",")


class TaskService:
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo

    def create_task(self, project_id: str, title: str, description: str = "", status: str = "todo", deadline_str: Optional[str] = None) -> TaskORM:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found.")

        title = title.strip()
        if not title:
            raise ValidationError("Task title cannot be empty.")
        if len(title) > TITLE_MAX:
            raise ValidationError(f"Task title length cannot exceed {TITLE_MAX}.")
        if len(description) > DESC_MAX:
            raise ValidationError(f"Description length cannot exceed {DESC_MAX}.")
        if status not in STATUS_VALUES:
            raise ValidationError(f"Invalid status. Must be one of: {', '.join(STATUS_VALUES)}")

        # Count total tasks across all projects
        total_tasks = sum(len(p.tasks) for p in self.project_repo.get_all())
        if total_tasks >= MAX_NUMBER_OF_TASK:
            raise ValidationError("Maximum number of tasks reached.")

        deadline = None
        if deadline_str:
            try:
                deadline = datetime.fromisoformat(deadline_str).date()
            except ValueError:
                raise ValidationError("Invalid date format. Use YYYY-MM-DD.")

        task = TaskORM(
            title=title,
            description=description.strip(),
            status=status,
            deadline=deadline,
            project_id=project_id
        )
        return self.task_repo.add(task)

    def get_task(self, task_id: str) -> TaskORM:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found.")
        return task

    def update_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None,
                   status: Optional[str] = None, deadline_str: Optional[str] = None) -> TaskORM:
        task = self.get_task(task_id)
        if title is not None:
            title = title.strip()
            if not title:
                raise ValidationError("Task title cannot be empty.")
            if len(title) > TITLE_MAX:
                raise ValidationError(f"Task title length cannot exceed {TITLE_MAX}.")
            task.title = title
        if description is not None:
            if len(description) > DESC_MAX:
                raise ValidationError(f"Description length cannot exceed {DESC_MAX}.")
            task.description = description
        if status is not None:
            if status not in STATUS_VALUES:
                raise ValidationError(f"Invalid status. Must be one of: {', '.join(STATUS_VALUES)}")
            task.status = status
        if deadline_str is not None:
            if deadline_str == "":
                task.deadline = None
            else:
                try:
                    task.deadline = datetime.fromisoformat(deadline_str).date()
                except ValueError:
                    raise ValidationError("Invalid date format. Use YYYY-MM-DD.")
        return self.task_repo.update(task)

    def delete_task(self, task_id: str) -> None:
        task = self.get_task(task_id)
        self.task_repo.delete(task)

    def list_tasks_by_project(self, project_id: str) -> List[TaskORM]:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found.")
        return self.task_repo.get_by_project_id(project_id)

    def close_overdue_tasks(self) -> int:
        """Close overdue tasks and return the count."""
        return self.task_repo.close_overdue_tasks()
