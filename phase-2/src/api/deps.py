"""API dependencies for dependency injection."""
from typing import Generator
from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.database import engine
from src.models.user import User
from src.services.auth_service import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
auth_service = AuthService()


def get_db() -> Generator[Session, None, None]:
    """Dependency for getting database sessions.

    Yields:
        Session: SQLModel database session

    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.exec(select(Item)).all()
    """
    with Session(engine) as session:
        yield session


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Dependency for getting the current authenticated user.

    Args:
        token: JWT access token from Authorization header
        db: Database session

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: 401 if token is invalid or user not found

    Example:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = auth_service.verify_token(token)
    if not token_data or not token_data.user_id:
        raise credentials_exception

    user = auth_service.get_user_by_id(db, token_data.user_id)
    if not user:
        raise credentials_exception

    return user
