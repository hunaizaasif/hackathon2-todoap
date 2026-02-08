"""CLI command handlers for Todo application."""

import cmd

from src.cli.display import format_error_message, format_success_message, format_task_list
from src.services.task_service import TaskService
from src.utils.validators import TaskNotFoundError, ValidationError, validate_task_id


class TodoCLI(cmd.Cmd):
    """Interactive CLI for managing todo tasks.

    Attributes:
        prompt: Command prompt string
        task_service: Service for managing tasks
    """

    prompt = "todo> "
    intro = "Welcome to CLI Todo!\nType 'help' for available commands or 'exit' to quit.\n"

    def __init__(self):
        """Initialize the CLI with a new task service."""
        super().__init__()
        self.task_service = TaskService()

    def do_add(self, arg: str) -> None:
        """Add a new task.

        Usage: add <description>

        Args:
            arg: Task description
        """
        if not arg:
            print(format_error_message("Task description cannot be empty"))
            return

        try:
            task = self.task_service.add_task(arg)
            print(format_success_message(f"Task added successfully (ID: {task.id})"))
        except ValidationError as e:
            print(format_error_message(str(e)))

    def do_list(self, arg: str) -> None:
        """Display all tasks.

        Usage: list
        """
        tasks = self.task_service.get_all_tasks()
        print(format_task_list(tasks))

    def do_complete(self, arg: str) -> None:
        """Mark a task as complete.

        Usage: complete <id>

        Args:
            arg: Task ID
        """
        if not arg:
            print(format_error_message("Task ID is required"))
            return

        try:
            task_id = validate_task_id(arg)
            task = self.task_service.get_task(task_id)

            if task.status.value == "complete":
                print(format_success_message(f"Task {task_id} is already complete"))
            else:
                self.task_service.mark_complete(task_id)
                print(format_success_message(f"Task {task_id} marked as complete"))
        except ValidationError as e:
            print(format_error_message(str(e)))
        except TaskNotFoundError as e:
            print(format_error_message(str(e)))

    def do_update(self, arg: str) -> None:
        """Update a task's description.

        Usage: update <id> <new_description>

        Args:
            arg: Task ID and new description
        """
        parts = arg.split(maxsplit=1)
        if len(parts) < 2:
            print(format_error_message("Usage: update <id> <new_description>"))
            return

        task_id_str, new_description = parts

        try:
            task_id = validate_task_id(task_id_str)
            self.task_service.update_task(task_id, new_description)
            print(format_success_message(f"Task {task_id} updated successfully"))
        except ValidationError as e:
            print(format_error_message(str(e)))
        except TaskNotFoundError as e:
            print(format_error_message(str(e)))

    def do_delete(self, arg: str) -> None:
        """Delete a task.

        Usage: delete <id>

        Args:
            arg: Task ID
        """
        if not arg:
            print(format_error_message("Task ID is required"))
            return

        try:
            task_id = validate_task_id(arg)
            self.task_service.delete_task(task_id)
            print(format_success_message(f"Task {task_id} deleted successfully"))
        except ValidationError as e:
            print(format_error_message(str(e)))
        except TaskNotFoundError as e:
            print(format_error_message(str(e)))

    def do_exit(self, arg: str) -> bool:
        """Exit the application.

        Usage: exit
        """
        print("Goodbye!")
        return True

    def do_quit(self, arg: str) -> bool:
        """Exit the application (alias for exit).

        Usage: quit
        """
        return self.do_exit(arg)

    def do_EOF(self, arg: str) -> bool:  # noqa: N802
        """Handle Ctrl+D to exit."""
        print()  # Print newline for clean exit
        return self.do_exit(arg)

    def help_add(self) -> None:
        """Display help for add command."""
        print(
            """
add <description>
    Add a new task with the given description.

    Arguments:
        description: Task description text (1-500 characters)

    Example:
        add Buy groceries
"""
        )

    def help_list(self) -> None:
        """Display help for list command."""
        print(
            """
list
    Display all tasks with their ID, description, and status.

    Example:
        list
"""
        )

    def help_complete(self) -> None:
        """Display help for complete command."""
        print(
            """
complete <id>
    Mark a task as complete.

    Arguments:
        id: Task ID (positive integer)

    Example:
        complete 1
"""
        )

    def help_update(self) -> None:
        """Display help for update command."""
        print(
            """
update <id> <new_description>
    Update a task's description.

    Arguments:
        id: Task ID (positive integer)
        new_description: New description text (1-500 characters)

    Example:
        update 1 Buy groceries and cook dinner
"""
        )

    def help_delete(self) -> None:
        """Display help for delete command."""
        print(
            """
delete <id>
    Delete a task permanently.

    Arguments:
        id: Task ID (positive integer)

    Example:
        delete 1
"""
        )

    def help_exit(self) -> None:
        """Display help for exit command."""
        print(
            """
exit
    Exit the application.

    Aliases: quit, Ctrl+D
"""
        )

    def get_names(self) -> list[str]:
        """Get list of command names, excluding EOF from help display."""
        names = super().get_names()
        # Filter out do_EOF so it doesn't appear in help listing
        return [name for name in names if name != "do_EOF"]

    def emptyline(self) -> None:
        """Do nothing on empty line (override default behavior)."""
        pass

    def default(self, line: str) -> None:
        """Handle unknown commands."""
        message = f"Unknown command '{line}'. Type 'help' for available commands."
        print(format_error_message(message))
