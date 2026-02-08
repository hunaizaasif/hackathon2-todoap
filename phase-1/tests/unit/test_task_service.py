"""Unit tests for TaskService."""

import pytest

from src.models.task import TaskStatus
from src.services.task_service import TaskService
from src.utils.validators import TaskNotFoundError, ValidationError


def test_add_task_success():
    """Test adding a task successfully."""
    service = TaskService()
    task = service.add_task("Buy groceries")

    assert task.id == 1
    assert task.description == "Buy groceries"
    assert task.status == TaskStatus.PENDING


def test_add_task_increments_id():
    """Test that task IDs increment correctly."""
    service = TaskService()
    task1 = service.add_task("First task")
    task2 = service.add_task("Second task")
    task3 = service.add_task("Third task")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3


def test_add_task_empty_description_raises_error():
    """Test that adding task with empty description raises ValidationError."""
    service = TaskService()
    with pytest.raises(ValidationError, match="Task description cannot be empty"):
        service.add_task("")


def test_add_task_too_long_description_raises_error():
    """Test that adding task with too long description raises ValidationError."""
    service = TaskService()
    long_description = "a" * 501
    with pytest.raises(ValidationError, match="cannot exceed 500 characters"):
        service.add_task(long_description)


def test_get_all_tasks_empty():
    """Test getting all tasks when none exist."""
    service = TaskService()
    tasks = service.get_all_tasks()

    assert tasks == []


def test_get_all_tasks_returns_all():
    """Test getting all tasks returns all added tasks."""
    service = TaskService()
    service.add_task("Task 1")
    service.add_task("Task 2")
    service.add_task("Task 3")

    tasks = service.get_all_tasks()

    assert len(tasks) == 3
    assert tasks[0].description == "Task 1"
    assert tasks[1].description == "Task 2"
    assert tasks[2].description == "Task 3"


def test_get_all_tasks_preserves_insertion_order():
    """Test that get_all_tasks preserves insertion order."""
    service = TaskService()
    service.add_task("First")
    service.add_task("Second")
    service.add_task("Third")

    tasks = service.get_all_tasks()

    assert [t.id for t in tasks] == [1, 2, 3]


def test_get_task_success():
    """Test getting a task by ID."""
    service = TaskService()
    added_task = service.add_task("Test task")

    retrieved_task = service.get_task(added_task.id)

    assert retrieved_task.id == added_task.id
    assert retrieved_task.description == added_task.description


def test_get_task_not_found_raises_error():
    """Test that getting non-existent task raises TaskNotFoundError."""
    service = TaskService()

    with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
        service.get_task(999)


def test_mark_complete_success():
    """Test marking a task as complete."""
    service = TaskService()
    task = service.add_task("Test task")

    assert task.status == TaskStatus.PENDING

    updated_task = service.mark_complete(task.id)

    assert updated_task.status == TaskStatus.COMPLETE
    assert updated_task.id == task.id


def test_mark_complete_idempotent():
    """Test that marking already complete task is idempotent."""
    service = TaskService()
    task = service.add_task("Test task")

    service.mark_complete(task.id)
    service.mark_complete(task.id)  # Mark complete again

    retrieved_task = service.get_task(task.id)
    assert retrieved_task.status == TaskStatus.COMPLETE


def test_mark_complete_not_found_raises_error():
    """Test that marking non-existent task raises TaskNotFoundError."""
    service = TaskService()

    with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
        service.mark_complete(999)


def test_update_task_success():
    """Test updating a task description."""
    service = TaskService()
    task = service.add_task("Original description")

    updated_task = service.update_task(task.id, "Updated description")

    assert updated_task.description == "Updated description"
    assert updated_task.id == task.id


def test_update_task_empty_description_raises_error():
    """Test that updating with empty description raises ValidationError."""
    service = TaskService()
    task = service.add_task("Original description")

    with pytest.raises(ValidationError, match="Task description cannot be empty"):
        service.update_task(task.id, "")


def test_update_task_not_found_raises_error():
    """Test that updating non-existent task raises TaskNotFoundError."""
    service = TaskService()

    with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
        service.update_task(999, "New description")


def test_delete_task_success():
    """Test deleting a task."""
    service = TaskService()
    task = service.add_task("Test task")

    service.delete_task(task.id)

    with pytest.raises(TaskNotFoundError):
        service.get_task(task.id)


def test_delete_task_not_found_raises_error():
    """Test that deleting non-existent task raises TaskNotFoundError."""
    service = TaskService()

    with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
        service.delete_task(999)


def test_delete_task_does_not_affect_other_tasks():
    """Test that deleting one task doesn't affect others."""
    service = TaskService()
    task1 = service.add_task("Task 1")
    task2 = service.add_task("Task 2")
    task3 = service.add_task("Task 3")

    service.delete_task(task2.id)

    tasks = service.get_all_tasks()
    assert len(tasks) == 2
    assert task1.id in [t.id for t in tasks]
    assert task3.id in [t.id for t in tasks]
    assert task2.id not in [t.id for t in tasks]
