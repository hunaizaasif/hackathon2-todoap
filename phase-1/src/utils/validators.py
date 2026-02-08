"""Custom exception classes and validation utilities for CLI Todo application."""


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass


class TaskNotFoundError(Exception):
    """Raised when task ID is not found."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


def validate_task_id(task_id_str: str) -> int:
    """Validate and parse task ID.

    Args:
        task_id_str: String representation of task ID

    Returns:
        Parsed integer task ID

    Raises:
        ValidationError: If task ID is invalid
    """
    try:
        task_id = int(task_id_str)
        if task_id < 1:
            raise ValidationError("Task ID must be a positive integer")
        return task_id
    except ValueError:
        raise ValidationError("Task ID must be a positive integer")


def validate_description(description: str) -> None:
    """Validate task description.

    Args:
        description: Task description text

    Raises:
        ValidationError: If description is invalid
    """
    if not description or not description.strip():
        raise ValidationError("Task description cannot be empty")
    if len(description) > 500:
        raise ValidationError(
            f"Task description cannot exceed 500 characters (got {len(description)})"
        )
