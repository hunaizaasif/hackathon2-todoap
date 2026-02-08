# Data Model: Phase 1 CLI Todo

**Feature**: 001-cli-todo | **Date**: 2026-02-05 | **Phase**: Design (Phase 1)

## Overview

This document defines the data entities and their relationships for the Phase 1 CLI Todo application. The model is intentionally simple to support in-memory storage while establishing a foundation that can be extended with persistence in Phase 2 (Todo Full-Stack Web Application).

## Core Entities

### Task

Represents a single todo item with a unique identifier, description, and completion status.

**Attributes**:

| Attribute | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| id | int | Yes | Positive integer, unique | Auto-generated unique identifier |
| description | str | Yes | 1-500 characters, non-empty | Task description text |
| status | TaskStatus | Yes | PENDING or COMPLETE | Current task status |

**Validation Rules**:
- `description` must not be empty (after stripping whitespace)
- `description` must not exceed 500 characters
- `id` must be positive integer (>= 1)
- `status` must be valid TaskStatus enum value

**Default Values**:
- `status`: TaskStatus.PENDING (all new tasks start as pending)

**Invariants**:
- Once created, a task's `id` never changes
- A task can only transition from PENDING to COMPLETE (not reversible in Phase 1)

**Python Implementation**:
```python
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    """Enumeration of possible task statuses."""
    PENDING = "pending"
    COMPLETE = "complete"

@dataclass
class Task:
    """Represents a single todo item."""
    id: int
    description: str
    status: TaskStatus

    def __post_init__(self):
        """Validate task attributes after initialization."""
        if not self.description or not self.description.strip():
            raise ValueError("Task description cannot be empty")
        if len(self.description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")
        if self.id < 1:
            raise ValueError("Task ID must be positive")
```

---

### TaskStatus (Enum)

Enumeration representing the possible states of a task.

**Values**:

| Value | String Representation | Description |
|-------|----------------------|-------------|
| PENDING | "pending" | Task is not yet complete (default state) |
| COMPLETE | "complete" | Task has been marked as complete |

**State Transitions**:
```
PENDING → COMPLETE (allowed via "complete" command)
COMPLETE → PENDING (not allowed in Phase 1)
```

**Display Format**:
- PENDING: Display as "Pending" in list view
- COMPLETE: Display as "Complete" in list view

**Python Implementation**:
```python
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETE = "complete"

    def __str__(self) -> str:
        """Return human-readable status string."""
        return self.value.capitalize()
```

---

## Data Storage

### In-Memory Storage Structure

**Primary Storage**: Dictionary with task ID as key

```python
tasks: dict[int, Task] = {}
```

**Rationale**:
- O(1) lookup by ID for update/delete/complete operations
- Maintains insertion order (Python 3.7+) for list display
- Simple and efficient for up to 100 tasks

**ID Generation**:
```python
next_id: int = 1  # Counter for generating unique IDs
```

**Operations**:
- **Add**: `tasks[next_id] = task; next_id += 1`
- **Get**: `tasks[id]` (raises KeyError if not found)
- **Get All**: `list(tasks.values())` (preserves insertion order)
- **Update**: `tasks[id].description = new_description`
- **Delete**: `del tasks[id]`
- **Complete**: `tasks[id].status = TaskStatus.COMPLETE`

---

## Entity Relationships

### Phase 1 (Current)

No relationships - single entity model.

```
┌──────────────┐
│     Task     │
├─────────────┤
│ id: int      │
│ description  │
│ status       │
└──────────────┘
```

### Phase 2 (Todo Full-Stack Web Application) - Future

Potential extensions for persistence layer:

```
┌──────────────┐
│     Task     │
├──────────────┤
│ id: int (PK) │
│ description  │
│ status       │
│ created_at   │ ← New field
│ updated_at   │ ← New field
└──────────────┘
```

### Phase 3 (Future)

Potential extensions for multi-user support:

```
┌──────────────┐         ┌──────────────┐
│     User     │         │     Task     │
├──────────────┤         ├──────────────┤
│ id: int (PK) │◄────────│ id: int (PK) │
│ username     │ 1     * │ user_id (FK) │
│ email        │         │ description  │
└──────────────┘         │ status       │
                         └──────────────┘
```

---

## Validation Rules

### Task Description Validation

**Rules**:
1. Must not be empty or whitespace-only
2. Must not exceed 500 characters
3. Must be valid UTF-8 string

**Error Messages**:
- Empty: "Task description cannot be empty"
- Too long: "Task description cannot exceed 500 characters (got {length})"

**Implementation**:
```python
def validate_description(description: str) -> None:
    """Validate task description."""
    if not description or not description.strip():
        raise ValidationError("Task description cannot be empty")
    if len(description) > 500:
        raise ValidationError(
            f"Task description cannot exceed 500 characters (got {len(description)})"
        )
```

### Task ID Validation

**Rules**:
1. Must be positive integer (>= 1)
2. Must exist in storage (for update/delete/complete operations)

**Error Messages**:
- Invalid format: "Task ID must be a positive integer"
- Not found: "Task with ID {id} not found"

**Implementation**:
```python
def validate_task_id(task_id: str) -> int:
    """Validate and parse task ID."""
    try:
        id_int = int(task_id)
        if id_int < 1:
            raise ValidationError("Task ID must be a positive integer")
        return id_int
    except ValueError:
        raise ValidationError("Task ID must be a positive integer")
```

---

## Data Constraints

### Phase 1 Constraints

1. **Session-Only**: Data exists only during application runtime
2. **Single-User**: No concurrent access or user isolation
3. **No Persistence**: Data lost when application exits
4. **Scale Limit**: Designed for up to 100 tasks (no hard limit enforced)

### Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Add Task | O(1) | O(1) |
| Get Task by ID | O(1) | O(1) |
| Get All Tasks | O(n) | O(n) |
| Update Task | O(1) | O(1) |
| Delete Task | O(1) | O(1) |
| Mark Complete | O(1) | O(1) |

**Memory Usage**: ~100 bytes per task (approximate)
- 100 tasks ≈ 10 KB
- 1000 tasks ≈ 100 KB

---

## Error Handling

### Domain Exceptions

**ValidationError**:
- Raised when: Invalid input (empty description, invalid ID format)
- Handled by: CLI layer displays error message to user

**TaskNotFoundError**:
- Raised when: Task ID doesn't exist in storage
- Handled by: CLI layer displays "Task with ID {id} not found"

**Python Implementation**:
```python
class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

class TaskNotFoundError(Exception):
    """Raised when task ID is not found."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")
```

---

## Migration Path to Phase 2 (Todo Full-Stack Web Application)

### Persistence Layer

Phase 2 (Todo Full-Stack Web Application) will add database persistence while maintaining the same domain model:

**Changes Required**:
1. Add `created_at` and `updated_at` timestamp fields
2. Map Task entity to database table (SQLModel)
3. Replace in-memory dict with database queries
4. Maintain same public API (add, get, update, delete, complete)

**Backward Compatibility**:
- CLI interface remains unchanged
- Task entity structure compatible (add optional fields)
- ID strategy compatible (database auto-increment)

**Example SQLModel Mapping**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str = Field(max_length=500)
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Summary

The Phase 1 data model is intentionally minimal:
- Single entity (Task) with three attributes
- Simple enum for status (PENDING/COMPLETE)
- In-memory dictionary storage
- Auto-incrementing integer IDs

This foundation supports all Phase 1 requirements while remaining extensible for future phases (persistence, multi-user, additional fields).

---

**Document Status**: Complete
**Last Updated**: 2026-02-05
**Next Review**: Before Phase 2 (Todo Full-Stack Web Application) planning
