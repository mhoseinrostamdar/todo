from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional
import uuid
import textwrap
import os
from dotenv import load_dotenv

load_dotenv()

MAX_NUMBER_OF_PROJECT= os.getenv("MAX_NUMBER_OF_PROJECT")
MAX_NUMBER_OF_TASK=os.getenv("MAX_NUMBER_OF_TASK")
TITLE_MAX=os.getenv("TITLE_MAX")
DESC_MAX=os.getenv("DESC_MAX")
STATUS_VALUES=os.getenv("STATUS_VALUES")

def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

# ===== Models =====
@dataclass
class Task:
    title: str
    description: str = ""
    status: str = "todo"
    deadline: Optional[date] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

    def set_status(self, status: str) -> None:
        self.status = status
        self.updated_at = now_iso()

    def set_deadline_from_str(self, date_str: str) -> None:
        if not date_str:
            self.deadline = None
            self.updated_at = now_iso()
            return
        try:
            self.deadline = datetime.fromisoformat(date_str).date()
            self.updated_at = now_iso()
        except Exception:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    def update(self, title=None, description=None, status=None, deadline_str=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if status is not None:
            self.set_status(status)
        if deadline_str is not None:
            self.set_deadline_from_str(deadline_str)
        self.updated_at = now_iso()


@dataclass
class Project:
    name: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tasks: dict[str, Task] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

    def add_task(self, task: Task):
        self.tasks[task.id] = task
        self.updated_at = now_iso()

    def remove_task(self, task_id: str):
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.updated_at = now_iso()
        else:
            raise KeyError("Task not found.")


