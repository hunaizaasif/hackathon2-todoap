"""Display formatting functions for CLI output."""

from src.models.task import Task


def format_success_message(message: str) -> str:
    """Format a success message with checkmark.

    Args:
        message: Success message text

    Returns:
        Formatted success message
    """
    return f"✓ {message}"


def format_error_message(message: str) -> str:
    """Format an error message.

    Args:
        message: Error message text

    Returns:
        Formatted error message
    """
    return f"Error: {message}"


def format_task_list(tasks: list[Task]) -> str:
    """Format a list of tasks as a table.

    Args:
        tasks: List of tasks to format

    Returns:
        Formatted task list as string
    """
    if not tasks:
        return "No tasks found. Use 'add <description>' to create a task."

    # Table header
    lines = []
    lines.append("ID  Description              Status")
    lines.append("─" * 40)

    # Table rows
    for task in tasks:
        # Truncate description if too long (max 25 chars for display)
        description = task.description
        if len(description) > 25:
            description = description[:22] + "..."

        # Format row with fixed column widths
        row = f"{task.id:<4}{description:<25}{str(task.status):<10}"
        lines.append(row)

    return "\n".join(lines)
