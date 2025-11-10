from sqlalchemy.orm import Session
from typing import Optional, List
from app.models import ProjectORM, TaskORM


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, project: ProjectORM) -> ProjectORM:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: str) -> Optional[ProjectORM]:
        return self.db.query(ProjectORM).filter(ProjectORM.id == project_id).first()

    def get_by_name(self, name: str) -> Optional[ProjectORM]:
        return self.db.query(ProjectORM).filter(ProjectORM.name == name).first()

    def get_all(self) -> List[ProjectORM]:
        return self.db.query(ProjectORM).all()

    def update(self, project: ProjectORM) -> ProjectORM:
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: ProjectORM) -> None:
        self.db.delete(project)
        self.db.commit()
