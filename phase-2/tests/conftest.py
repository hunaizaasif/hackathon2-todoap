"""Pytest configuration and fixtures."""
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from src.models.user import User
from src.models.task import Task


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session.

    Yields:
        Session: SQLModel database session for testing
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """Create a test user.

    Args:
        session: Database session

    Returns:
        User: Test user
    """
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_user_2")
def test_user_2_fixture(session: Session):
    """Create a second test user.

    Args:
        session: Database session

    Returns:
        User: Second test user
    """
    user = User(
        email="test2@example.com",
        password_hash="hashed_password_2",
        name="Test User 2"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
