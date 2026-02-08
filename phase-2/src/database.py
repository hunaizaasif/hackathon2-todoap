"""Database connection and session management."""
from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool
from src.config import settings


# Create engine with connection pooling for Neon Serverless PostgreSQL
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=5,              # Max connections in pool
    max_overflow=10,          # Additional connections if pool exhausted
    pool_pre_ping=True,       # Verify connections before use
    pool_recycle=3600,        # Recycle connections after 1 hour
    echo=settings.debug,      # SQL logging in debug mode
)


def get_session():
    """Get a database session.

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session
