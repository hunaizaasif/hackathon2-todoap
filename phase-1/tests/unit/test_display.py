"""Unit tests for display formatting functions."""

from src.cli.display import format_error_message, format_success_message, format_task_list
from src.models.task import Task, TaskStatus


def test_format_success_message():
    """Test formatting success messages."""
    message = format_success_message("Task added successfully")
    assert "✓" in message
    assert "Task added successfully" in message


def test_format_error_message():
    """Test formatting error messages."""
    message = format_error_message("Task not found")
    assert "Error:" in message
    assert "Task not found" in message


def test_format_task_list_empty():
    """Test formatting empty task list."""
    output = format_task_list([])
    assert "No tasks found" in output
    assert "add <description>" in output


def test_format_task_list_single_task():
    """Test formatting list with single task."""
    tasks = [Task(id=1, description="Buy groceries", status=TaskStatus.PENDING)]
    output = format_task_list(tasks)

    assert "ID" in output
    assert "Description" in output
    assert "Status" in output
    assert "1" in output
    assert "Buy groceries" in output
    assert "Pending" in output


def test_format_task_list_multiple_tasks():
    """Test formatting list with multiple tasks."""
    tasks = [
        Task(id=1, description="Buy groceries", status=TaskStatus.PENDING),
        Task(id=2, description="Write documentation", status=TaskStatus.COMPLETE),
        Task(id=3, description="Review code", status=TaskStatus.PENDING),
    ]
    output = format_task_list(tasks)

    assert "1" in output
    assert "Buy groceries" in output
    assert "2" in output
    assert "Write documentation" in output
    assert "3" in output
    assert "Review code" in output
    assert output.count("Pending") == 2
    assert output.count("Complete") == 1


def test_format_task_list_long_description_truncated():
    """Test that long descriptions are truncated."""
    long_desc = "a" * 100
    tasks = [Task(id=1, description=long_desc, status=TaskStatus.PENDING)]
    output = format_task_list(tasks)

    # Description should be truncated with "..."
    assert "..." in output
    # Check that the full long description is not in the output
    assert long_desc not in output


def test_format_task_list_mixed_statuses():
    """Test formatting list with mixed task statuses."""
    tasks = [
        Task(id=1, description="Pending task", status=TaskStatus.PENDING),
        Task(id=2, description="Complete task", status=TaskStatus.COMPLETE),
    ]
    output = format_task_list(tasks)

    assert "Pending" in output
    assert "Complete" in output
