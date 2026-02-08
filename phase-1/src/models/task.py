"""Task model and status enum for CLI Todo application."""

from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""

    PENDING = "pending"
    COMPLETE = "complete"

    def __str__(self) -> str:
        """Return human-readable status string."""
        return self.value.capitalize()


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier for the task
        description: Task description text
        status: Current status (PENDING or COMPLETE)
    """

    id: int
    description: str
    status: TaskStatus

    def __post_init__(self):
        """Validate task attributes after initialization."""
        if not self.description or not self.description.strip():
            raise ValueError("Task description cannot be empty")
        if len(self.description) > 500:
            raise ValueError(
                f"Task description cannot exceed 500 characters (got {len(self.description)})"
            )
        if self.id < 1:
            raise ValueError("Task ID must be positive")
