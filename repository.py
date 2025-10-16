from typing import Optional
from models import Project
import os
from dotenv import load_dotenv

load_dotenv()

class Repository:
    def __init__(self):
        self.projects = {}
    def add_project(self, project: Project):
        self.projects[project.id] = project

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)

    def remove_project(self, project_id: str):
        if project_id in self.projects:
            del self.projects[project_id]
        else:
            raise KeyError("Project not found.")

    def list_projects(self):
        return list(self.projects.values())



