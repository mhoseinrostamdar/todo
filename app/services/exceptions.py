"""Domain-level exceptions used across services."""


class DomainError(Exception):
    """Base class for predictable business rule errors."""


class NotFoundError(DomainError):
    """Raised when an entity cannot be found."""


class ConflictError(DomainError):
    """Raised when a business rule prevents an operation (e.g., duplicates)."""


class ValidationError(DomainError):
    """Raised when input values violate validation constraints."""

