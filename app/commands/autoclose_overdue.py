import click
from app.db.session import get_db
from app.repositories import TaskRepository
from app.services import TaskService


@click.command()
def autoclose_overdue():
    """Automatically close overdue tasks."""
    db = next(get_db())
    try:
        task_repo = TaskRepository(db)
        project_repo = None  # Not needed for this operation
        task_service = TaskService(task_repo, project_repo)
        count = task_service.close_overdue_tasks()
        click.echo(f"Closed {count} overdue tasks.")
    finally:
        db.close()


if __name__ == "__main__":
    autoclose_overdue()
