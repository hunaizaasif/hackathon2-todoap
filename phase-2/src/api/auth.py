"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from src.api.deps import get_db
from src.schemas.user import UserRegister, UserLogin, UserResponse, Token
from src.services.auth_service import AuthService
from datetime import timedelta


router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user account.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        UserResponse: Created user

    Raises:
        HTTPException: 400 if email already exists
    """
    user = auth_service.register_user(db, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return access token.

    Args:
        form_data: OAuth2 password form (username=email, password)
        db: Database session

    Returns:
        Token: Access token and token type

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    user = auth_service.login_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", status_code=204)
def logout():
    """Logout user (JWT is stateless, so this is a no-op).

    Returns:
        None: 204 No Content

    Note:
        Since JWT tokens are stateless, logout is handled client-side
        by discarding the token. This endpoint exists for API completeness.
    """
    return None


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get current authenticated user information.

    Args:
        token: JWT access token
        db: Database session

    Returns:
        UserResponse: Current user information

    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    token_data = auth_service.verify_token(token)
    if not token_data or not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = auth_service.get_user_by_id(db, token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
