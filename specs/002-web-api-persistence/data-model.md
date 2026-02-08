# Data Model: Phase 2 - Todo Full-Stack Web Application

**Feature**: Phase 2 - Todo Full-Stack Web Application
**Date**: 2026-02-05
**Status**: Complete

## Overview

This document defines the database schema, entities, relationships, and validation rules for Phase 2 (Todo Full-Stack Web Application). The data model supports multi-user task management with authentication and user isolation.

---

## Database Schema

### Technology
- **Database**: PostgreSQL (Neon Serverless)
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Migration Tool**: Alembic

---

## Entities

### 1. User

Represents a registered user account with authentication credentials.

**Table Name**: `user`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address for authentication |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password (managed by Better Auth) |
| name | VARCHAR(100) | NULLABLE | User's display name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp (UTC) |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp (UTC) |

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` (for login lookups)

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    name: Optional[str] = Field(max_length=100, default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- Email must be valid email format (validated by Pydantic)
- Email must be unique across all users
- Password must be hashed before storage (never store plaintext)
- Name is optional but if provided, max 100 characters

**Business Rules**:
- Users cannot be deleted (out of scope for Phase 2)
- Email cannot be changed after registration (out of scope for Phase 2)
- Password changes handled by Better Auth (out of scope for Phase 2)

---

### 2. Task

Represents a todo item owned by a specific user.

**Table Name**: `task`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique task identifier |
| user_id | INTEGER | FOREIGN KEY (user.id), NOT NULL, INDEXED | Owner of this task |
| title | VARCHAR(200) | NOT NULL | Short task summary |
| description | TEXT | NULLABLE | Detailed task description (max 2000 chars) |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Task state: pending, in_progress, complete |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task creation timestamp (UTC) |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp (UTC) |

**Indexes**:
- Primary key index on `id` (automatic)
- Foreign key index on `user_id` (for user isolation queries)
- Composite index on `(user_id, status)` (for filtered queries)

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, Literal

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(max_length=2000, default=None)
    status: str = Field(default="pending", max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- Title: 1-200 characters, cannot be empty or whitespace-only
- Description: 0-2000 characters, optional
- Status: Must be one of: "pending", "in_progress", "complete"
- user_id: Must reference an existing user (foreign key constraint)

**Business Rules**:
- Tasks are always associated with exactly one user
- Tasks cannot be transferred between users (out of scope)
- Tasks cannot be shared or made public (out of scope)
- Deleted tasks are permanently removed (no soft delete)
- updated_at is automatically updated on any modification

---

## Relationships

### User → Task (One-to-Many)

- One user can have zero or many tasks
- Each task belongs to exactly one user
- Foreign key: `task.user_id` → `user.id`
- Cascade behavior: NOT DEFINED (user deletion out of scope for Phase 2)

**Query Pattern**:
```python
# Get all tasks for a user
statement = select(Task).where(Task.user_id == user_id)
tasks = session.exec(statement).all()

# Get user with their tasks (if relationship defined in SQLModel)
# Note: Explicit relationship not required for Phase 2, queries are sufficient
```

---

## State Transitions

### Task Status State Machine

```
┌─────────┐
│ pending │ (initial state)
└────┬────┘
     │
     ├──────────────┐
     │              │
     ▼              ▼
┌──────────────┐  ┌──────────┐
│ in_progress  │  │ complete │
└──────┬───────┘  └────▲─────┘
       │               │
       └───────────────┘
```

**Valid Transitions**:
- `pending` → `in_progress`
- `pending` → `complete` (skip in_progress)
- `in_progress` → `complete`
- `in_progress` → `pending` (restart)
- `complete` → `pending` (reopen)
- `complete` → `in_progress` (reopen and continue)

**Implementation Note**: Phase 2 does not enforce state transition rules. Any status can transition to any other status. State machine enforcement is out of scope but documented for future phases.

---

## Database Constraints

### Primary Keys
- `user.id`: Auto-incrementing integer
- `task.id`: Auto-incrementing integer

### Foreign Keys
- `task.user_id` → `user.id`
  - ON DELETE: NOT DEFINED (user deletion out of scope)
  - ON UPDATE: CASCADE (if user.id changes, update task.user_id)

### Unique Constraints
- `user.email`: Must be unique across all users

### Check Constraints
- `task.status`: Must be one of ('pending', 'in_progress', 'complete')
- `task.title`: Length between 1 and 200 characters
- `task.description`: Length between 0 and 2000 characters (if not null)

**Implementation Note**: SQLModel/Pydantic handles most validation at application level. Database constraints provide defense-in-depth.

---

## Indexes for Performance

### User Table
1. **Primary Key Index**: `user.id` (automatic)
2. **Email Index**: `user.email` (unique, for login queries)

### Task Table
1. **Primary Key Index**: `task.id` (automatic)
2. **User ID Index**: `task.user_id` (for user isolation queries)
3. **Composite Index**: `(user_id, status)` (for filtered queries like "get my pending tasks")

**Query Optimization**:
```sql
-- Optimized by user_id index
SELECT * FROM task WHERE user_id = 123;

-- Optimized by composite (user_id, status) index
SELECT * FROM task WHERE user_id = 123 AND status = 'pending';

-- Optimized by email index
SELECT * FROM user WHERE email = 'user@example.com';
```

---

## Migration Strategy

### Initial Schema Creation

**Migration 001**: Create users and tasks tables

```python
# alembic/versions/001_create_users_and_tasks.py
def upgrade():
    # Create user table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_user_email', 'user', ['email'])

    # Create task table
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'])
    )
    op.create_index('ix_task_user_id', 'task', ['user_id'])
    op.create_index('ix_task_user_id_status', 'task', ['user_id', 'status'])

def downgrade():
    op.drop_table('task')
    op.drop_table('user')
```

---

## Data Validation Summary

### Application-Level Validation (Pydantic/SQLModel)
- Type checking (int, str, datetime)
- String length constraints
- Email format validation
- Enum validation for status field
- Required vs optional fields

### Database-Level Validation (PostgreSQL)
- NOT NULL constraints
- UNIQUE constraints
- FOREIGN KEY constraints
- CHECK constraints (if implemented)
- Data type enforcement

**Defense-in-Depth**: Both layers provide validation. Application layer gives better error messages; database layer prevents data corruption.

---

## Sample Data

### Example User
```json
{
  "id": 1,
  "email": "alice@example.com",
  "password_hash": "$2b$12$...",
  "name": "Alice Smith",
  "created_at": "2026-02-05T10:00:00Z",
  "updated_at": "2026-02-05T10:00:00Z"
}
```

### Example Task
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Complete Phase 2 implementation",
  "description": "Implement FastAPI endpoints with SQLModel and Neon DB",
  "status": "in_progress",
  "created_at": "2026-02-05T10:30:00Z",
  "updated_at": "2026-02-05T11:00:00Z"
}
```

---

## Edge Cases and Constraints

### User Entity
- **Empty name**: Allowed (name is optional)
- **Duplicate email**: Rejected by unique constraint
- **Invalid email format**: Rejected by Pydantic validation
- **Missing password**: Rejected by NOT NULL constraint

### Task Entity
- **Empty title**: Rejected by min_length=1 validation
- **Whitespace-only title**: Should be rejected by custom validator
- **Description > 2000 chars**: Rejected by max_length validation
- **Invalid status**: Rejected by Pydantic Literal type
- **Non-existent user_id**: Rejected by foreign key constraint
- **Negative user_id**: Allowed by database but prevented by auth (user must exist)

### Concurrent Updates
- **Same task updated by two requests**: Last write wins (no optimistic locking in Phase 2)
- **Task deleted while being updated**: Update fails with 404 (task not found)

---

## Future Considerations (Out of Scope for Phase 2)

- **Soft deletes**: Add `deleted_at` column, filter out deleted records
- **Task categories/tags**: Many-to-many relationship with new `tag` table
- **Task sharing**: Add `task_share` table with user_id and task_id
- **Audit log**: Add `audit_log` table to track all changes
- **Task attachments**: Add `attachment` table with file references
- **User profiles**: Expand user table with avatar, bio, preferences
- **Task due dates**: Add `due_date` column to task table
- **Task priority**: Add `priority` enum column to task table

---

**Data Model Status**: ✅ Complete
**Next Step**: Generate API contracts (OpenAPI specification)
