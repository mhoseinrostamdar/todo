"""FastAPI controllers for project and task endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.controller_schemas.requests.project_request_schema import ProjectCreateRequest, ProjectUpdateRequest
from app.api.controller_schemas.requests.task_request_schema import (
    TaskCreateRequest,
    TaskStatusUpdateRequest,
    TaskUpdateRequest,
)
from app.api.controller_schemas.responses.project_response_schema import ProjectDetailResponse, ProjectResponse
from app.api.controller_schemas.responses.task_response_schema import TaskResponse
from app.db import get_session
from app.services import exceptions as exc
from app.services.project_service import ProjectService
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])


def get_project_service(session: Session = Depends(get_session)) -> ProjectService:
    return ProjectService(session)


def get_task_service(session: Session = Depends(get_session)) -> TaskService:
    return TaskService(session)


def _handle_domain_error(error: exc.DomainError) -> None:
    if isinstance(error, exc.NotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    if isinstance(error, exc.ValidationError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    if isinstance(error, exc.ConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")


@router.get("", response_model=list[ProjectResponse], summary="List projects")
def list_projects(service: ProjectService = Depends(get_project_service)):
    try:
        return service.list_projects()
    except exc.DomainError as error:
        _handle_domain_error(error)


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, summary="Create a project")
def create_project(payload: ProjectCreateRequest, service: ProjectService = Depends(get_project_service)):
    try:
        return service.create_project(name=payload.name, description=payload.description)
    except exc.DomainError as error:
        _handle_domain_error(error)


@router.get("/{project_id}", response_model=ProjectDetailResponse, summary="Get a project with its tasks")
def get_project(project_id: str, service: ProjectService = Depends(get_project_service)):
    try:
        return service.get_project(project_id)
    except exc.DomainError as error:
        _handle_domain_error(error)


@router.put("/{project_id}", response_model=ProjectResponse, summary="Update a project")
def update_project(project_id: str, payload: ProjectUpdateRequest, service: ProjectService = Depends(get_project_service)):
    try:
        data = payload.model_dump(exclude_unset=True)
        return service.update_project(project_id=project_id, **data)
    except exc.DomainError as error:
        _handle_domain_error(error)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a project")
def delete_project(project_id: str, service: ProjectService = Depends(get_project_service)):
    try:
        service.delete_project(project_id)
    except exc.DomainError as error:
        _handle_domain_error(error)


@router.get(
    "/{project_id}/tasks",
    response_model=list[TaskResponse],
    summary="List tasks for a project",
)
def list_tasks(project_id: str, service: TaskService = Depends(get_task_service)):
    try:
        return service.list_tasks(project_id)
    except exc.DomainError as error:
        _handle_domain_error(error)


@router.post(
    "/{project_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task under a project",
)
def create_task(project_id: str, payload: TaskCreateRequest, service: TaskService = Depends(get_task_service)):
    try:
        data = payload.model_dump()
        return service.create_task(project_id=project_id, **data)
    except exc.DomainError as error:
        _handle_domain_error(error)


@router.get(
    "/{project_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get a task",
)
def get_task(project_id: str, task_id: str, service: TaskService = Depends(get_task_service)):
    try:
        return service.get_task(project_id, task_id)
    except exc.DomainError as error:
        _handle_domain_error(error)


@router.put(
    "/{project_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
)
def update_task(project_id: str, task_id: str, payload: TaskUpdateRequest, service: TaskService = Depends(get_task_service)):
    try:
        data = payload.model_dump(exclude_unset=True)
        return service.update_task(project_id=project_id, task_id=task_id, **data)
    except exc.DomainError as error:
        _handle_domain_error(error)


@router.patch(
    "/{project_id}/tasks/{task_id}/status",
    response_model=TaskResponse,
    summary="Change task status",
)
def change_task_status(
    project_id: str, task_id: str, payload: TaskStatusUpdateRequest, service: TaskService = Depends(get_task_service)
):
    try:
        return service.change_status(project_id=project_id, task_id=task_id, status=payload.status)
    except exc.DomainError as error:
        _handle_domain_error(error)


@router.delete(
    "/{project_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(project_id: str, task_id: str, service: TaskService = Depends(get_task_service)):
    try:
        service.delete_task(project_id, task_id)
    except exc.DomainError as error:
        _handle_domain_error(error)

