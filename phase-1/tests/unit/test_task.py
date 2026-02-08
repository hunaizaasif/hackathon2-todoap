"""Unit tests for Task model."""

import pytest

from src.models.task import Task, TaskStatus


def test_task_creation_valid():
    """Test creating a valid task."""
    task = Task(id=1, description="Buy groceries", status=TaskStatus.PENDING)
    assert task.id == 1
    assert task.description == "Buy groceries"
    assert task.status == TaskStatus.PENDING


def test_task_status_string_representation():
    """Test TaskStatus string representation."""
    assert str(TaskStatus.PENDING) == "Pending"
    assert str(TaskStatus.COMPLETE) == "Complete"


def test_task_empty_description_raises_error():
    """Test that empty description raises ValueError."""
    with pytest.raises(ValueError, match="Task description cannot be empty"):
        Task(id=1, description="", status=TaskStatus.PENDING)


def test_task_whitespace_only_description_raises_error():
    """Test that whitespace-only description raises ValueError."""
    with pytest.raises(ValueError, match="Task description cannot be empty"):
        Task(id=1, description="   ", status=TaskStatus.PENDING)


def test_task_description_too_long_raises_error():
    """Test that description over 500 characters raises ValueError."""
    long_description = "a" * 501
    with pytest.raises(ValueError, match="cannot exceed 500 characters"):
        Task(id=1, description=long_description, status=TaskStatus.PENDING)


def test_task_description_exactly_500_chars_valid():
    """Test that description with exactly 500 characters is valid."""
    description = "a" * 500
    task = Task(id=1, description=description, status=TaskStatus.PENDING)
    assert len(task.description) == 500


def test_task_negative_id_raises_error():
    """Test that negative ID raises ValueError."""
    with pytest.raises(ValueError, match="Task ID must be positive"):
        Task(id=0, description="Test task", status=TaskStatus.PENDING)


def test_task_with_unicode_description():
    """Test task with unicode characters in description."""
    task = Task(id=1, description="Buy 🥖 and 🥐", status=TaskStatus.PENDING)
    assert task.description == "Buy 🥖 and 🥐"
