# create project
# add project
# delete project
# get projects
#...

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional
import uuid
import textwrap
import os
from dotenv import load_dotenv
from repository import Repository
from models import Task
from models import Project

load_dotenv()

MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT"))
MAX_NUMBER_OF_TASK = int(os.getenv("MAX_NUMBER_OF_TASK"))
TITLE_MAX = int(os.getenv("TITLE_MAX"))
DESC_MAX = int(os.getenv("DESC_MAX"))
STATUS_VALUES = os.getenv("STATUS_VALUES")

def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

# ===== Business Logic =====
class ToDoManager:
    def __init__(self, storage: Optional[Repository] = None):
        self.storage = storage or Repository()

    def create_project(self, name: str, description: str = "") -> Project:
        name = name.strip()
        if not name:
            raise ValueError("Project name cannot be empty.")
        if len(name) > TITLE_MAX:
            raise ValueError(f"Project name length cannot exceed {TITLE_MAX}.")
        for p in self.storage.list_projects():
            if p.name == name:
                raise ValueError("Project name already exists.")
        if len(self.storage.list_projects()) >= MAX_NUMBER_OF_PROJECT:
            raise ValueError("Maximum number of projects reached.")
        proj = Project(name=name, description=description.strip())
        self.storage.add_project(proj)
        return proj

    def edit_project(self, project_id: str, new_name=None, new_description=None) -> Project:
        proj = self.storage.get_project(project_id)
        if proj is None:
            raise KeyError("Project not found.")
        if new_name:
            if len(new_name) > TITLE_MAX:
                raise ValueError(f"Project name length cannot exceed {TITLE_MAX}.")
            for p in self.storage.list_projects():
                if p.id != proj.id and p.name == new_name:
                    raise ValueError("New project name already exists.")
            proj.name = new_name
        if new_description is not None:
            if len(new_description) > DESC_MAX:
                raise ValueError(f"Description length cannot exceed {DESC_MAX}.")
            proj.description = new_description
        proj.updated_at = now_iso()
        return proj

    def delete_project(self, project_id: str):
        proj = self.storage.get_project(project_id)
        if proj is None:
            raise KeyError("Project not found.")
        self.storage.remove_project(project_id)

    def list_projects(self):
        return self.storage.list_projects()

    def _count_all_tasks(self) -> int:
        return sum(len(p.tasks) for p in self.storage.list_projects())

    def add_task(self, project_id: str, title: str, description: str = "", status=None, deadline_str=None) -> Task:
        proj = self.storage.get_project(project_id)
        if proj is None:
            raise KeyError("Project not found.")
        if not title.strip():
            raise ValueError("Task title cannot be empty.")
        if len(title) > TITLE_MAX:
            raise ValueError(f"Task title length cannot exceed {TITLE_MAX}.")
        if len(description) > DESC_MAX:
            raise ValueError(f"Description length cannot exceed {DESC_MAX}.")
        if self._count_all_tasks() >= MAX_NUMBER_OF_TASK:
            raise ValueError("Maximum number of tasks reached.")
        t = Task(title=title.strip(), description=description.strip())
        if status:
            t.set_status(status)
        if deadline_str:
            t.set_deadline_from_str(deadline_str)
        proj.add_task(t)
        return t

    def edit_task(self, project_id: str, task_id: str, **kwargs) -> Task:
        proj = self.storage.get_project(project_id)
        if proj is None:
            raise KeyError("Project not found.")
        task = proj.tasks.get(task_id)
        if not task:
            raise KeyError("Task not found.")
        task.update(**kwargs)
        return task

    def delete_task(self, project_id: str, task_id: str):
        proj = self.storage.get_project(project_id)
        if proj is None:
            raise KeyError("Project not found.")
        if task_id not in proj.tasks:
            raise KeyError("Task not found.")
        proj.remove_task(task_id)

    def change_task_status(self, project_id: str, task_id: str, new_status: str) -> Task:
        proj = self.storage.get_project(project_id)
        if proj is None:
            raise KeyError("Project not found.")
        task = proj.tasks.get(task_id)
        if not task:
            raise KeyError("Task not found.")
        task.set_status(new_status)
        return task

    def list_tasks_of_project(self, project_id: str):
        proj = self.storage.get_project(project_id)
        if proj is None:
            raise KeyError("Project not found.")
        return list(proj.tasks.values())