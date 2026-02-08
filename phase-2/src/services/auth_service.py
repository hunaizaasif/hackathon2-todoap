"""Authentication service for user management."""
from sqlmodel import Session, select
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from src.models.user import User
from src.schemas.user import UserRegister, TokenData
from src.config import settings


# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    """Service class for authentication operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            str: Hashed password
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash.

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password

        Returns:
            bool: True if password matches, False otherwise
        """
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token.

        Args:
            data: Data to encode in the token
            expires_delta: Optional expiration time delta

        Returns:
            str: Encoded JWT token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.auth_secret_key, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[TokenData]:
        """Verify and decode a JWT token.

        Args:
            token: JWT token string

        Returns:
            Optional[TokenData]: Token data if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, settings.auth_secret_key, algorithms=[ALGORITHM])
            user_id_str: str = payload.get("sub")
            email: str = payload.get("email")
            if user_id_str is None:
                return None
            # Convert string user_id back to int
            user_id = int(user_id_str)
            return TokenData(user_id=user_id, email=email)
        except (JWTError, ValueError, TypeError):
            return None

    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> Optional[User]:
        """Register a new user.

        Args:
            db: Database session
            user_data: User registration data

        Returns:
            Optional[User]: Created user if successful, None if email already exists
        """
        # Check if user already exists
        statement = select(User).where(User.email == user_data.email)
        existing_user = db.exec(statement).first()
        if existing_user:
            return None

        # Create new user
        hashed_password = AuthService.hash_password(user_data.password)
        user = User(
            email=user_data.email,
            password_hash=hashed_password,
            name=user_data.name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password.

        Args:
            db: Database session
            email: User email
            password: Plain text password

        Returns:
            Optional[User]: User if authentication successful, None otherwise
        """
        statement = select(User).where(User.email == email)
        user = db.exec(statement).first()
        if not user:
            return None
        if not AuthService.verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get a user by ID.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Optional[User]: User if found, None otherwise
        """
        statement = select(User).where(User.id == user_id)
        return db.exec(statement).first()
