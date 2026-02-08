"""Pydantic schemas for Task API requests and responses."""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Literal


class TaskCreate(BaseModel):
    """Schema for creating a new task.

    Attributes:
        title: Task title (1-200 characters, required)
        description: Task description (max 2000 characters, optional)
        status: Task status (pending, in_progress, complete)
    """

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(max_length=2000, default=None)
    status: Literal["pending", "in_progress", "complete"] = "pending"

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate that title is not empty or whitespace only."""
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip()


class TaskUpdate(BaseModel):
    """Schema for updating an existing task (full update).

    Attributes:
        title: Task title (1-200 characters, required)
        description: Task description (max 2000 characters, optional)
        status: Task status (pending, in_progress, complete)
    """

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(max_length=2000, default=None)
    status: Literal["pending", "in_progress", "complete"]

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate that title is not empty or whitespace only."""
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip()


class TaskPatch(BaseModel):
    """Schema for partially updating a task.

    Attributes:
        title: Task title (1-200 characters, optional)
        description: Task description (max 2000 characters, optional)
        status: Task status (pending, in_progress, complete, optional)
    """

    title: Optional[str] = Field(min_length=1, max_length=200, default=None)
    description: Optional[str] = Field(max_length=2000, default=None)
    status: Optional[Literal["pending", "in_progress", "complete"]] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate that title is not empty or whitespace only if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip() if v else None


class TaskResponse(BaseModel):
    """Schema for task API responses.

    Attributes:
        id: Task ID
        user_id: User ID who owns this task
        title: Task title
        description: Task description
        status: Task status
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: int
    user_id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
