# Phase 1 CLI Todo Application

A simple command-line interface (CLI) todo application built with Python 3.13+ that provides core task management functionality with in-memory storage.

## Features

- ✅ Add new tasks with descriptions
- ✅ List all tasks with their status
- ✅ Mark tasks as complete
- ✅ Update task descriptions
- ✅ Delete tasks
- ✅ Interactive REPL interface
- ✅ Comprehensive error handling
- ✅ 85%+ test coverage

## Requirements

- Python 3.13 or higher
- UV package manager

## Installation

### 1. Install Python 3.13+

Download and install Python 3.13 or higher from [python.org](https://www.python.org/downloads/).

Verify installation:
```bash
python --version
# Should output: Python 3.13.x or higher
```

### 2. Install UV Package Manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify installation:
```bash
uv --version
```

### 3. Navigate to Project Directory

```bash
cd phase-1
```

### 4. Install Dependencies

```bash
uv sync
```

This will:
- Create a virtual environment at `.venv`
- Install all development dependencies (pytest, pytest-cov, ruff)

## Usage

### Start the Application

```bash
uv run python src/main.py
```

You should see:
```
Welcome to CLI Todo!
Type 'help' for available commands or 'exit' to quit.

todo>
```

### Available Commands

#### Add a Task
```bash
todo> add Buy groceries
✓ Task added successfully (ID: 1)
```

#### List All Tasks
```bash
todo> list
ID  Description              Status
────────────────────────────────────────
1   Buy groceries            Pending
```

#### Mark Task as Complete
```bash
todo> complete 1
✓ Task 1 marked as complete
```

#### Update Task Description
```bash
todo> update 1 Buy groceries and cook dinner
✓ Task 1 updated successfully
```

#### Delete a Task
```bash
todo> delete 1
✓ Task 1 deleted successfully
```

#### Get Help
```bash
todo> help
```

For help on a specific command:
```bash
todo> help add
```

#### Exit the Application
```bash
todo> exit
Goodbye!
```

You can also use `quit` or press `Ctrl+D` to exit.

## Example Session

```bash
$ uv run python src/main.py
Welcome to CLI Todo!
Type 'help' for available commands or 'exit' to quit.

todo> add Review pull requests
✓ Task added successfully (ID: 1)

todo> add Write documentation
✓ Task added successfully (ID: 2)

todo> add Team meeting at 2pm
✓ Task added successfully (ID: 3)

todo> list
ID  Description              Status
────────────────────────────────────────
1   Review pull requests     Pending
2   Write documentation      Pending
3   Team meeting at 2pm      Pending

todo> complete 1
✓ Task 1 marked as complete

todo> list
ID  Description              Status
────────────────────────────────────────
1   Review pull requests     Complete
2   Write documentation      Pending
3   Team meeting at 2pm      Pending

todo> update 2 Write comprehensive documentation
✓ Task 2 updated successfully

todo> delete 3
✓ Task 3 deleted successfully

todo> list
ID  Description              Status
────────────────────────────────────────
1   Review pull requests     Complete
2   Write comprehensive...   Pending

todo> exit
Goodbye!
```

## Important Notes

### Data Persistence

⚠️ **WARNING**: All tasks are stored in memory only. When you exit the application, all data is lost. This is intentional for Phase 1.

**Phase 2 (Todo Full-Stack Web Application)** will add database persistence to save tasks between sessions.

### Task ID Behavior

- Task IDs are auto-incrementing integers starting at 1
- IDs are assigned when tasks are created
- Deleting a task does NOT reuse its ID
- IDs reset when the application restarts

### Character Limits

- Task descriptions: Maximum 500 characters
- Longer descriptions will be rejected with an error message
- Descriptions displayed in list view are truncated to 25 characters with "..."

### Special Characters

- Task descriptions support UTF-8 characters (emojis, accented characters, etc.)
- Example: `add Buy 🥖 and 🥐` works correctly

## Development

### Running Tests

Run all tests with coverage:
```bash
uv run pytest tests/ --cov=src --cov-report=term-missing
```

Run only unit tests:
```bash
uv run pytest tests/unit/
```

Run only integration tests:
```bash
uv run pytest tests/integration/
```

Run specific test file:
```bash
uv run pytest tests/unit/test_task_service.py
```

### Code Quality

Check code with linter:
```bash
uv run ruff check src/ tests/
```

Format code:
```bash
uv run ruff format src/ tests/
```

### Project Structure

```
phase-1/
├── src/
│   ├── main.py              # Application entry point
│   ├── models/
│   │   └── task.py          # Task entity and TaskStatus enum
│   ├── services/
│   │   └── task_service.py  # Business logic for CRUD operations
│   ├── cli/
│   │   ├── commands.py      # Command handlers (add, list, etc.)
│   │   └── display.py       # Output formatting
│   └── utils/
│       └── validators.py    # Input validation logic
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── pyproject.toml           # UV project configuration
├── .python-version          # Python version specification
└── README.md                # This file
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

## Testing Coverage

Current test coverage: **85%**

- 53 tests passing
- Unit tests: 40 tests
- Integration tests: 13 tests

Coverage by module:
- `src/cli/display.py`: 100%
- `src/models/task.py`: 100%
- `src/services/task_service.py`: 100%
- `src/utils/validators.py`: 100%
- `src/cli/commands.py`: 76% (help methods not covered)

## Performance

- All operations complete in under 1 second for up to 100 tasks
- Memory usage: ~10 KB for 100 tasks
- Designed for up to 100 tasks without performance degradation

## Next Steps (Phase 2 - Todo Full-Stack Web Application)

Phase 2 (Todo Full-Stack Web Application) will add:
- Database persistence (PostgreSQL with Neon)
- Web API (FastAPI)
- Authentication (Better Auth)
- Data persistence across sessions

## License

This is a learning project for the Hackathon-2 event.

## Contributing

This is Phase 1 of a multi-phase project. All work is contained in the `/phase-1` directory per project requirements.
