# Research & Technical Decisions: Phase 1 CLI Todo

**Feature**: 001-cli-todo | **Date**: 2026-02-05 | **Phase**: Research (Phase 0)

## Overview

This document consolidates research findings and technical decisions made during the planning phase for the Phase 1 CLI Todo application. All decisions prioritize simplicity, maintainability, and alignment with Phase 1 scope while establishing a foundation for future phases.

## Research Areas

### 1. Python CLI Best Practices

**Research Question**: What are the best practices for building command-line interfaces in Python?

**Findings**:
- **REPL Pattern**: Interactive Read-Eval-Print Loop provides better UX for multi-command sessions
- **cmd Module**: Python's built-in `cmd` module provides robust REPL support with minimal code
- **Error Handling**: CLI applications should never crash; all errors should be caught and displayed with actionable messages
- **Exit Codes**: Use standard exit codes (0 for success, 1 for errors)
- **User Feedback**: Provide immediate, clear feedback for every action

**Sources**:
- Python cmd module documentation
- Click and Typer library patterns (for reference, not using)
- Unix CLI design principles

**Application to Project**:
- Use cmd.Cmd base class for REPL interface
- Implement graceful error handling at CLI layer
- Provide consistent success/error message formatting
- Use standard exit codes

---

### 2. Clean Code Principles for Python

**Research Question**: What Clean Code principles apply to Python CLI applications?

**Findings**:
- **Function Size**: Keep functions under 20 lines; single responsibility principle
- **Naming**: Use descriptive names (PEP 8): snake_case for functions/variables, PascalCase for classes
- **Error Handling**: Use custom exceptions for domain errors; avoid generic Exception catches
- **Type Hints**: Use type hints for function signatures (Python 3.13 supports modern syntax)
- **Docstrings**: Document public APIs with docstrings; comments for complex logic only

**Sources**:
- Clean Code by Robert C. Martin (adapted for Python)
- PEP 8 - Style Guide for Python Code
- PEP 484 - Type Hints

**Application to Project**:
- All functions <20 lines
- Type hints on all function signatures
- Custom exception classes (ValidationError, TaskNotFoundError)
- Docstrings for public functions
- Ruff for automated linting/formatting

---

### 3. In-Memory Data Structure Design

**Research Question**: What's the optimal data structure for storing tasks in memory?

**Findings**:
- **List**: O(n) lookup, O(1) append, maintains order
- **Dictionary**: O(1) lookup by key, maintains insertion order (Python 3.7+)
- **Hybrid**: Both structures for different access patterns (adds complexity)

**Performance Analysis** (for 100 tasks):
- List lookup: ~100 operations worst case
- Dict lookup: ~1 operation (hash table)
- Memory overhead: Negligible difference for 100 items

**Decision**: Dictionary with integer ID as key
- O(1) lookup for update/delete/complete operations
- Maintains insertion order for list display
- Simpler than maintaining two structures
- Sufficient for Phase 1 scope (up to 100 tasks)

**Application to Project**:
```python
tasks: dict[int, Task] = {}
next_id: int = 1
```

---

### 4. UV Package Manager

**Research Question**: How to properly initialize and configure a UV project?

**Findings**:
- **Initialization**: `uv init` creates pyproject.toml with modern Python packaging
- **Dependencies**: Separate dev dependencies from runtime dependencies
- **Python Version**: Specify exact Python version in .python-version file
- **Virtual Environments**: UV automatically manages virtual environments
- **Lock Files**: UV creates uv.lock for reproducible builds

**UV Commands**:
- `uv init` - Initialize project
- `uv add <package>` - Add runtime dependency
- `uv add --dev <package>` - Add development dependency
- `uv run <command>` - Run command in UV environment
- `uv sync` - Sync dependencies from lock file

**Application to Project**:
```toml
[project]
name = "cli-todo"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "pytest-cov>=4.1.0", "ruff>=0.1.0"]
```

---

### 5. Testing Strategy

**Research Question**: What testing approach ensures comprehensive coverage for a CLI application?

**Findings**:
- **Unit Tests**: Test individual components in isolation (models, services, validators)
- **Integration Tests**: Test end-to-end command flows with real interactions
- **Coverage Target**: 90%+ is achievable and maintainable for small projects
- **Test Organization**: Mirror source structure (tests/unit/, tests/integration/)
- **Mocking**: Use unittest.mock for isolating components in unit tests

**pytest Best Practices**:
- Use fixtures for common setup (task service, sample tasks)
- Parametrize tests for multiple input scenarios
- Use pytest-cov for coverage reporting
- Organize tests by component, not by test type

**Application to Project**:
```
tests/
├── unit/
│   ├── test_task.py          # Task model tests
│   ├── test_task_service.py  # Service layer tests
│   ├── test_validators.py    # Validation logic tests
│   └── test_display.py       # Display formatting tests
└── integration/
    └── test_cli_commands.py  # End-to-end CLI tests
```

**Coverage Target**: 90%+ line coverage

---

## Key Technical Decisions

### Decision 1: CLI Interface Pattern

**Decision**: Interactive REPL using Python's cmd module

**Options Considered**:
1. **Interactive REPL** (Selected)
   - Pros: Better UX for multiple operations, natural fit for session-based data
   - Cons: Less familiar to some CLI users
2. **Single-command execution** (e.g., `todo add "task"`)
   - Pros: Familiar Unix pattern, scriptable
   - Cons: Poor UX for multiple operations, doesn't align with session-only data
3. **Hybrid approach**
   - Pros: Flexibility
   - Cons: Increased complexity, harder to maintain

**Rationale**:
- Session-only data retention aligns perfectly with REPL session lifecycle
- Better user experience for managing multiple tasks in one session
- Simpler error recovery (user stays in application)
- cmd module provides built-in REPL support with minimal code

**Implementation Details**:
- Extend `cmd.Cmd` class
- Implement `do_<command>` methods for each operation
- Use built-in help system
- Custom prompt: `todo> `

---

### Decision 2: Task ID Strategy

**Decision**: Auto-incrementing integer starting at 1

**Options Considered**:
1. **Auto-incrementing integer** (Selected)
   - Pros: User-friendly, easy to type, sufficient for single-session
   - Cons: Not globally unique (not needed for Phase 1)
2. **UUID**
   - Pros: Globally unique
   - Cons: Hard to type, overkill for in-memory single-session use
3. **Hash-based ID**
   - Pros: Deterministic
   - Cons: Collision risk, complexity

**Rationale**:
- User-friendly: Easy to type "complete 3" vs "complete a7b3c..."
- Sufficient: No collision risk in single-user, single-session context
- Aligns with user expectations for simple CLI tools
- Prepares for Phase 2 (Todo Full-Stack Web Application): Can map to database auto-increment primary key

**Implementation Details**:
```python
class TaskService:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, description: str) -> Task:
        task = Task(id=self._next_id, description=description, status=TaskStatus.PENDING)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task
```

---

### Decision 3: Data Storage Structure

**Decision**: Dictionary with ID as key, Task as value

**Options Considered**:
1. **List of Task objects**
   - Pros: Simple, maintains order
   - Cons: O(n) lookup for update/delete/complete
2. **Dictionary with ID as key** (Selected)
   - Pros: O(1) lookup, maintains insertion order (Python 3.7+)
   - Cons: Slightly more complex than list
3. **Both (list + dict)**
   - Pros: Optimized for all access patterns
   - Cons: Unnecessary complexity, maintenance burden

**Rationale**:
- O(1) lookup critical for update/delete/complete operations
- Python 3.7+ dicts maintain insertion order (no need for separate list)
- Simpler than maintaining two synchronized structures
- Performance sufficient for 100 tasks

**Implementation Details**:
```python
tasks: dict[int, Task] = {}
# Insertion order preserved for list display
for task in tasks.values():
    print(task)
```

---

### Decision 4: Command Parsing Approach

**Decision**: Python cmd module with do_* methods

**Options Considered**:
1. **argparse with subcommands**
   - Pros: Standard library, powerful
   - Cons: Designed for single-command execution, not REPL
2. **Custom string parsing**
   - Pros: Full control
   - Cons: Reinventing the wheel, error-prone
3. **cmd module** (Selected)
   - Pros: Built-in REPL support, clean separation, built-in help
   - Cons: Less flexible than argparse

**Rationale**:
- Built-in support for REPL pattern (perfect fit)
- Clean command handler separation (do_add, do_list, etc.)
- Built-in help system (automatic from docstrings)
- No external dependencies
- Extensible for future commands

**Implementation Details**:
```python
class TodoCLI(cmd.Cmd):
    prompt = "todo> "

    def do_add(self, arg):
        """Add a new task: add <description>"""
        # Implementation

    def do_list(self, arg):
        """List all tasks: list"""
        # Implementation
```

---

### Decision 5: Testing Strategy

**Decision**: Both unit and integration tests with pytest

**Options Considered**:
1. **Unit tests only**
   - Pros: Fast, isolated
   - Cons: Doesn't verify end-to-end flows
2. **Integration tests only**
   - Pros: Verifies real behavior
   - Cons: Slow, hard to debug, incomplete coverage
3. **Both unit and integration** (Selected)
   - Pros: Comprehensive coverage, fast feedback, confidence
   - Cons: More tests to maintain

**Rationale**:
- Unit tests verify individual components (models, services, validators)
- Integration tests verify end-to-end command flows
- Comprehensive coverage ensures reliability
- Supports refactoring with confidence
- Fast feedback loop (unit tests run in milliseconds)

**Implementation Details**:
- Unit tests: Test each module in isolation with mocks
- Integration tests: Test CLI commands end-to-end
- Coverage target: 90%+
- Run with: `pytest tests/ --cov=src --cov-report=term-missing`

---

## Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| Language | Python | 3.13+ | Specified in requirements, modern features |
| Package Manager | UV | Latest | Specified in requirements, fast and reliable |
| CLI Framework | cmd module | Built-in | REPL support, no dependencies |
| Data Model | dataclasses | Built-in | Clean syntax, type hints |
| Testing | pytest | 8.0+ | Industry standard, rich ecosystem |
| Coverage | pytest-cov | 4.1+ | Integrated with pytest |
| Linting/Formatting | ruff | 0.1+ | Fast, replaces multiple tools |

---

## Alternatives Considered and Rejected

### Click/Typer for CLI
**Rejected**: These are excellent frameworks but designed for single-command execution, not REPL. The cmd module is a better fit for our interactive session-based model.

### SQLite for Storage
**Rejected**: Phase 1 explicitly requires in-memory storage. SQLite would be appropriate for Phase 2 (Todo Full-Stack Web Application - persistence).

### unittest Instead of pytest
**Rejected**: pytest provides better fixtures, parametrization, and plugin ecosystem. More modern and maintainable.

### JSON/YAML Configuration
**Rejected**: No configuration needed for Phase 1. Keep it simple.

---

## Open Questions Resolved

1. **Q**: Should we support command-line arguments for non-interactive use?
   **A**: No. Phase 1 focuses on interactive REPL. Single-command execution can be added in future phases if needed.

2. **Q**: Should we validate task description length?
   **A**: Yes. Set reasonable limit (e.g., 500 characters) to prevent abuse and ensure good display formatting.

3. **Q**: Should we support task priorities or categories?
   **A**: No. Out of scope for Phase 1. Focus on core CRUD operations only.

4. **Q**: Should we persist data to a file?
   **A**: No. Phase 1 explicitly requires in-memory only. Persistence is Phase 2 (Todo Full-Stack Web Application).

5. **Q**: Should we support undo/redo?
   **A**: No. Out of scope for Phase 1. Keep it simple.

---

## Next Steps

1. ✅ Research complete - All technical decisions documented
2. → Create data-model.md with detailed entity definitions
3. → Create contracts/cli-interface.md with command specifications
4. → Create quickstart.md with setup and usage instructions
5. → Update agent context with technology stack
6. → Generate tasks.md with `/sp.tasks` command

---

**Document Status**: Complete
**Last Updated**: 2026-02-05
**Approved By**: Planning phase
