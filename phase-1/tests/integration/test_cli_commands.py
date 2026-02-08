"""Integration tests for CLI commands."""

from io import StringIO
from unittest.mock import patch

from src.cli.commands import TodoCLI


def test_add_and_list_commands():
    """Test adding tasks and listing them."""
    cli = TodoCLI()

    # Add tasks
    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_add("Buy groceries")
        output = fake_out.getvalue()
        assert "Task added successfully (ID: 1)" in output

    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_add("Write documentation")
        output = fake_out.getvalue()
        assert "Task added successfully (ID: 2)" in output

    # List tasks
    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_list("")
        output = fake_out.getvalue()
        assert "Buy groceries" in output
        assert "Write documentation" in output
        assert "Pending" in output


def test_add_empty_description():
    """Test adding task with empty description."""
    cli = TodoCLI()

    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_add("")
        output = fake_out.getvalue()
        assert "Error:" in output
        assert "cannot be empty" in output


def test_list_empty():
    """Test listing when no tasks exist."""
    cli = TodoCLI()

    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_list("")
        output = fake_out.getvalue()
        assert "No tasks found" in output


def test_complete_command():
    """Test marking task as complete."""
    cli = TodoCLI()

    # Add a task
    cli.do_add("Test task")

    # Mark it complete
    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_complete("1")
        output = fake_out.getvalue()
        assert "marked as complete" in output

    # Verify status in list
    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_list("")
        output = fake_out.getvalue()
        assert "Complete" in output


def test_complete_already_complete():
    """Test marking already complete task."""
    cli = TodoCLI()

    cli.do_add("Test task")
    cli.do_complete("1")

    # Try to complete again
    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_complete("1")
        output = fake_out.getvalue()
        assert "already complete" in output


def test_complete_invalid_id():
    """Test completing with invalid ID."""
    cli = TodoCLI()

    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_complete("abc")
        output = fake_out.getvalue()
        assert "Error:" in output
        assert "positive integer" in output


def test_complete_nonexistent_id():
    """Test completing non-existent task."""
    cli = TodoCLI()

    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_complete("999")
        output = fake_out.getvalue()
        assert "Error:" in output
        assert "not found" in output


def test_update_command():
    """Test updating task description."""
    cli = TodoCLI()

    cli.do_add("Original description")

    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_update("1 Updated description")
        output = fake_out.getvalue()
        assert "updated successfully" in output

    # Verify in list
    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_list("")
        output = fake_out.getvalue()
        assert "Updated description" in output
        assert "Original description" not in output


def test_update_invalid_usage():
    """Test update with invalid usage."""
    cli = TodoCLI()

    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_update("1")
        output = fake_out.getvalue()
        assert "Usage:" in output


def test_delete_command():
    """Test deleting a task."""
    cli = TodoCLI()

    cli.do_add("Task to delete")
    cli.do_add("Task to keep")

    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_delete("1")
        output = fake_out.getvalue()
        assert "deleted successfully" in output

    # Verify task is gone
    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_list("")
        output = fake_out.getvalue()
        assert "Task to delete" not in output
        assert "Task to keep" in output


def test_delete_nonexistent_id():
    """Test deleting non-existent task."""
    cli = TodoCLI()

    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.do_delete("999")
        output = fake_out.getvalue()
        assert "Error:" in output
        assert "not found" in output


def test_exit_command():
    """Test exit command."""
    cli = TodoCLI()

    with patch("sys.stdout", new=StringIO()) as fake_out:
        result = cli.do_exit("")
        output = fake_out.getvalue()
        assert "Goodbye!" in output
        assert result is True


def test_unknown_command():
    """Test handling unknown command."""
    cli = TodoCLI()

    with patch("sys.stdout", new=StringIO()) as fake_out:
        cli.default("unknown")
        output = fake_out.getvalue()
        assert "Unknown command" in output
        assert "help" in output
