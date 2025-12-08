"""Repository for Project entities."""
from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Project


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_projects(self) -> Iterable[Project]:
        stmt = select(Project).order_by(Project.created_at)
        return self.session.scalars(stmt).all()

    def get(self, project_id: str) -> Optional[Project]:
        return self.session.get(Project, project_id)

    def get_by_name(self, name: str) -> Optional[Project]:
        stmt = select(Project).where(Project.name == name)
        return self.session.scalars(stmt).first()

    def add(self, project: Project) -> Project:
        self.session.add(project)
        self.session.flush()
        return project

    def delete(self, project: Project) -> None:
        self.session.delete(project)

    def count(self) -> int:
        stmt = select(func.count(Project.id))
        return self.session.execute(stmt).scalar_one()

