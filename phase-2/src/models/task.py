"""Task model for todo items."""
from sqlmodel import SQLModel, Field, Index
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """Task entity representing a todo item.

    Attributes:
        id: Unique task identifier (auto-generated)
        user_id: Foreign key reference to the user who owns this task
        title: Short summary of the task (1-200 characters, required)
        description: Detailed description of the task (0-2000 characters, optional)
        status: Current state of the task (pending, in_progress, complete)
        created_at: Task creation timestamp (UTC)
        updated_at: Last update timestamp (UTC)
    """

    __table_args__ = (
        Index('ix_task_user_id_status', 'user_id', 'status'),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(max_length=2000, default=None)
    status: str = Field(default="pending", max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
