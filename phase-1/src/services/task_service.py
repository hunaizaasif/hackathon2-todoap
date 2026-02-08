"""Task service for managing todo tasks in memory."""

from src.models.task import Task, TaskStatus
from src.utils.validators import TaskNotFoundError, validate_description


class TaskService:
    """Service for managing tasks with in-memory storage.

    Attributes:
        _tasks: Dictionary storing tasks by ID
        _next_id: Counter for generating unique task IDs
    """

    def __init__(self):
        """Initialize the task service with empty storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, description: str) -> Task:
        """Add a new task with the given description.

        Args:
            description: Task description text

        Returns:
            The newly created task

        Raises:
            ValidationError: If description is invalid
        """
        validate_description(description)
        task = Task(id=self._next_id, description=description, status=TaskStatus.PENDING)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks in insertion order.

        Returns:
            List of all tasks
        """
        return list(self._tasks.values())

    def get_task(self, task_id: int) -> Task:
        """Get a task by ID.

        Args:
            task_id: Task ID to retrieve

        Returns:
            The requested task

        Raises:
            TaskNotFoundError: If task ID doesn't exist
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as complete.

        Args:
            task_id: Task ID to mark complete

        Returns:
            The updated task

        Raises:
            TaskNotFoundError: If task ID doesn't exist
        """
        task = self.get_task(task_id)
        task.status = TaskStatus.COMPLETE
        return task

    def update_task(self, task_id: int, new_description: str) -> Task:
        """Update a task's description.

        Args:
            task_id: Task ID to update
            new_description: New description text

        Returns:
            The updated task

        Raises:
            TaskNotFoundError: If task ID doesn't exist
            ValidationError: If new description is invalid
        """
        validate_description(new_description)
        task = self.get_task(task_id)
        task.description = new_description
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task.

        Args:
            task_id: Task ID to delete

        Raises:
            TaskNotFoundError: If task ID doesn't exist
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        del self._tasks[task_id]
