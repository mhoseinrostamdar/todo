"""Repository for Task entities."""
from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Task


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_for_project(self, project_id: str) -> Iterable[Task]:
        stmt = select(Task).where(Task.project_id == project_id).order_by(Task.created_at)
        return self.session.scalars(stmt).all()

    def get(self, task_id: str) -> Optional[Task]:
        return self.session.get(Task, task_id)

    def add(self, task: Task) -> Task:
        self.session.add(task)
        self.session.flush()
        return task

    def delete(self, task: Task) -> None:
        self.session.delete(task)

    def count_all(self) -> int:
        stmt = select(func.count(Task.id))
        return self.session.execute(stmt).scalar_one()

