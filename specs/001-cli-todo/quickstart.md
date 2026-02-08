# Quickstart Guide: Phase 1 CLI Todo

**Feature**: 001-cli-todo | **Date**: 2026-02-05 | **Version**: 1.0.0

## Overview

Phase 1 CLI Todo is a simple command-line todo application built with Python 3.13+. It provides an interactive REPL interface for managing tasks with in-memory storage (data is not persisted between sessions).

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13 or higher**: [Download Python](https://www.python.org/downloads/)
- **UV package manager**: [Install UV](https://github.com/astral-sh/uv)

### Verify Installation

```bash
# Check Python version
python --version
# Should output: Python 3.13.x or higher

# Check UV installation
uv --version
# Should output: uv x.x.x
```

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/Hackathon-2/phase-1
```

### Step 2: Initialize UV Project (First Time Only)

```bash
# Initialize UV project
uv init

# Sync dependencies
uv sync
```

### Step 3: Install Development Dependencies

```bash
# Install testing and linting tools
uv add --dev pytest pytest-cov ruff
```

## Running the Application

### Start the Interactive CLI

```bash
# Run with UV
uv run python src/main.py
```

You should see:
```
Welcome to CLI Todo!
Type 'help' for available commands or 'exit' to quit.

todo>
```

## Basic Usage

### Add a Task

```bash
todo> add Buy groceries
✓ Task added successfully (ID: 1)
```

### List All Tasks

```bash
todo> list
ID  Description              Status
──────────────────────────────────────
1   Buy groceries            Pending
```

### Mark Task as Complete

```bash
todo> complete 1
✓ Task 1 marked as complete

todo> list
ID  Description              Status
──────────────────────────────────────
1   Buy groceries            Complete
```

### Update Task Description

```bash
todo> update 1 Buy groceries and cook dinner
✓ Task 1 updated successfully
```

### Delete a Task

```bash
todo> delete 1
✓ Task 1 deleted successfully
```

### Get Help

```bash
todo> help
Available commands:
  add <description>       Add a new task
  list                    Display all tasks
  update <id> <desc>      Update task description
  complete <id>           Mark task as complete
  delete <id>             Delete a task
  help [command]          Show this help message
  exit                    Exit the application
```

### Exit the Application

```bash
todo> exit
Goodbye!
```

## Common Workflows

### Workflow 1: Daily Task Management

```bash
# Start application
uv run python src/main.py

# Add today's tasks
todo> add Review pull requests
✓ Task added successfully (ID: 1)

todo> add Write documentation
✓ Task added successfully (ID: 2)

todo> add Team meeting at 2pm
✓ Task added successfully (ID: 3)

# View all tasks
todo> list
ID  Description              Status
──────────────────────────────────────
1   Review pull requests     Pending
2   Write documentation      Pending
3   Team meeting at 2pm      Pending

# Complete tasks as you finish them
todo> complete 1
✓ Task 1 marked as complete

# Check progress
todo> list
ID  Description              Status
──────────────────────────────────────
1   Review pull requests     Complete
2   Write documentation      Pending
3   Team meeting at 2pm      Pending

# Exit when done
todo> exit
Goodbye!
```

### Workflow 2: Task Refinement

```bash
# Add a task with initial description
todo> add Buy stuff
✓ Task added successfully (ID: 1)

# Realize you need more detail
todo> update 1 Buy groceries: milk, eggs, bread
✓ Task 1 updated successfully

# Verify the update
todo> list
ID  Description              Status
──────────────────────────────────────
1   Buy groceries: milk...   Pending
```

### Workflow 3: Task Cleanup

```bash
# List all tasks
todo> list
ID  Description              Status
──────────────────────────────────────
1   Old task                 Complete
2   Current task             Pending
3   Cancelled task           Pending

# Delete completed or cancelled tasks
todo> delete 1
✓ Task 1 deleted successfully

todo> delete 3
✓ Task 3 deleted successfully

# Verify cleanup
todo> list
ID  Description              Status
──────────────────────────────────────
2   Current task             Pending
```

## Running Tests

### Run All Tests

```bash
# Run full test suite with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing
```

### Run Unit Tests Only

```bash
uv run pytest tests/unit/
```

### Run Integration Tests Only

```bash
uv run pytest tests/integration/
```

### Run Specific Test File

```bash
uv run pytest tests/unit/test_task_service.py
```

## Code Quality

### Run Linter

```bash
# Check code quality
uv run ruff check src/ tests/

# Auto-fix issues
uv run ruff check --fix src/ tests/
```

### Run Formatter

```bash
# Format code
uv run ruff format src/ tests/
```

## Troubleshooting

### Issue: "Python 3.13 not found"

**Solution**: Install Python 3.13 or higher from [python.org](https://www.python.org/downloads/)

### Issue: "uv: command not found"

**Solution**: Install UV package manager:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Issue: "Module not found" errors

**Solution**: Ensure dependencies are installed:
```bash
cd phase-1
uv sync
```

### Issue: Application crashes on startup

**Solution**: Check Python version and ensure you're in the correct directory:
```bash
python --version  # Should be 3.13+
pwd               # Should end with /phase-1
```

### Issue: Tasks disappear after closing application

**Expected Behavior**: Phase 1 uses in-memory storage only. Tasks are not persisted between sessions. This is by design. Persistence will be added in Phase 2 (Todo Full-Stack Web Application).

## Important Notes

### Data Persistence

⚠️ **WARNING**: All tasks are stored in memory only. When you exit the application, all data is lost. This is intentional for Phase 1.

**Phase 2 (Todo Full-Stack Web Application)** will add database persistence to save tasks between sessions.

### Task ID Behavior

- Task IDs are auto-incrementing integers starting at 1
- IDs are assigned when tasks are created
- Deleting a task does NOT reuse its ID
- IDs reset when the application restarts

**Example**:
```bash
todo> add Task 1
✓ Task added successfully (ID: 1)

todo> add Task 2
✓ Task added successfully (ID: 2)

todo> delete 1
✓ Task 1 deleted successfully

todo> add Task 3
✓ Task added successfully (ID: 3)  # ID 1 is NOT reused
```

### Character Limits

- Task descriptions: Maximum 500 characters
- Longer descriptions will be rejected with an error message

### Special Characters

- Task descriptions support UTF-8 characters (emojis, accented characters, etc.)
- Example: `add Buy 🥖 and 🥐` works correctly

## Project Structure

```
phase-1/
├── src/
│   ├── main.py              # Application entry point
│   ├── models/
│   │   └── task.py          # Task entity and status enum
│   ├── services/
│   │   └── task_service.py  # Business logic
│   ├── cli/
│   │   ├── commands.py      # Command handlers
│   │   └── display.py       # Output formatting
│   └── utils/
│       └── validators.py    # Input validation
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── pyproject.toml           # UV project configuration
└── README.md                # Detailed documentation
```

## Next Steps

After completing Phase 1:

1. **Phase 2 (Todo Full-Stack Web Application)**: Add web API and database persistence
2. **Phase 3**: Integrate AI agent capabilities
3. **Phase 4**: Deploy to cloud with Kubernetes
4. **Phase 5**: Add event-driven architecture

## Getting Help

- **Command Help**: Type `help` in the application
- **Detailed Help**: Type `help <command>` for specific command help
- **Documentation**: See `README.md` in the phase-1 directory
- **Issues**: Report bugs or request features via project issue tracker

## Quick Reference Card

| Command | Syntax | Example |
|---------|--------|---------|
| Add task | `add <description>` | `add Buy groceries` |
| List tasks | `list` | `list` |
| Update task | `update <id> <description>` | `update 1 New description` |
| Complete task | `complete <id>` | `complete 1` |
| Delete task | `delete <id>` | `delete 1` |
| Help | `help [command]` | `help add` |
| Exit | `exit` | `exit` |

## Performance Notes

- Designed for up to 100 tasks without performance degradation
- All operations complete in under 1 second
- Memory usage: ~10 KB for 100 tasks

## Development Workflow

### Making Changes

1. Make code changes in `src/`
2. Run tests: `uv run pytest tests/`
3. Check code quality: `uv run ruff check src/`
4. Format code: `uv run ruff format src/`
5. Run application: `uv run python src/main.py`

### Adding New Commands

1. Add command handler in `src/cli/commands.py`
2. Add tests in `tests/integration/test_cli_commands.py`
3. Update help text
4. Update this quickstart guide

---

**Document Status**: Complete
**Last Updated**: 2026-02-05
**Maintained By**: Phase 1 development team
