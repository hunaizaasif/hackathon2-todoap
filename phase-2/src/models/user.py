"""User model for authentication and user management."""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    """User entity representing a registered user account.

    Attributes:
        id: Unique user identifier (auto-generated)
        email: User's email address (unique, required for authentication)
        password_hash: Bcrypt hashed password (managed by Better Auth)
        name: User's display name (optional)
        created_at: Account creation timestamp (UTC)
        updated_at: Last update timestamp (UTC)
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    name: Optional[str] = Field(max_length=100, default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
