from sqlalchemy.orm import Session
from typing import Optional, List
from app.models import TaskORM
from datetime import datetime


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, task: TaskORM) -> TaskORM:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: str) -> Optional[TaskORM]:
        return self.db.query(TaskORM).filter(TaskORM.id == task_id).first()

    def get_by_project_id(self, project_id: str) -> List[TaskORM]:
        return self.db.query(TaskORM).filter(TaskORM.project_id == project_id).all()

    def get_all(self) -> List[TaskORM]:
        return self.db.query(TaskORM).all()

    def update(self, task: TaskORM) -> TaskORM:
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: TaskORM) -> None:
        self.db.delete(task)
        self.db.commit()

    def get_overdue_tasks(self) -> List[TaskORM]:
        """Get tasks that are overdue and not done."""
        now = datetime.utcnow().date()
        return self.db.query(TaskORM).filter(
            TaskORM.deadline < now,
            TaskORM.status != 'done'
        ).all()

    def close_overdue_tasks(self) -> int:
        """Close overdue tasks and return the count of closed tasks."""
        overdue_tasks = self.get_overdue_tasks()
        count = 0
        for task in overdue_tasks:
            task.status = 'done'
            task.closed_at = datetime.utcnow()
            count += 1
        self.db.commit()
        return count
