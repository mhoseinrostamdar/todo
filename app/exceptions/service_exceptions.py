from .base import ToDoAppError


class ValidationError(ToDoAppError):
    """Raised when validation fails."""
    pass


class NotFoundError(ToDoAppError):
    """Raised when a resource is not found."""
    pass
