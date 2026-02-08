"""Main entry point for CLI Todo application."""

from src.cli.commands import TodoCLI


def main():
    """Run the CLI Todo application."""
    cli = TodoCLI()
    cli.cmdloop()


if __name__ == "__main__":
    main()
