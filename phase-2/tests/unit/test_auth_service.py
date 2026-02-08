"""Unit tests for AuthService."""
import pytest
from sqlmodel import Session
from src.models.user import User
from src.services.auth_service import AuthService
from src.schemas.user import UserRegister


class TestAuthService:
    """Test suite for AuthService."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "test_password_123"
        hashed = AuthService.hash_password(password)

        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")  # bcrypt hash prefix

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "test_password_123"
        hashed = AuthService.hash_password(password)

        result = AuthService.verify_password(password, hashed)
        assert result is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = AuthService.hash_password(password)

        result = AuthService.verify_password(wrong_password, hashed)
        assert result is False

    def test_create_access_token(self):
        """Test JWT token creation."""
        data = {"sub": 1, "email": "test@example.com"}
        token = AuthService.create_access_token(data)

        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)

    def test_verify_token_valid(self):
        """Test verifying a valid JWT token."""
        data = {"sub": "1", "email": "test@example.com"}
        token = AuthService.create_access_token(data)

        token_data = AuthService.verify_token(token)

        assert token_data is not None
        assert token_data.user_id == 1
        assert token_data.email == "test@example.com"

    def test_verify_token_invalid(self):
        """Test verifying an invalid JWT token."""
        invalid_token = "invalid.token.here"

        token_data = AuthService.verify_token(invalid_token)
        assert token_data is None

    def test_verify_token_expired(self):
        """Test verifying an expired JWT token."""
        from datetime import timedelta

        data = {"sub": 1, "email": "test@example.com"}
        # Create token that expires immediately
        token = AuthService.create_access_token(data, expires_delta=timedelta(seconds=-1))

        token_data = AuthService.verify_token(token)
        assert token_data is None

    def test_register_user_success(self, session: Session):
        """Test successful user registration."""
        user_data = UserRegister(
            email="newuser@example.com",
            password="secure_password_123",
            name="New User"
        )

        user = AuthService.register_user(session, user_data)

        assert user is not None
        assert user.id is not None
        assert user.email == "newuser@example.com"
        assert user.name == "New User"
        assert user.password_hash != "secure_password_123"  # Password should be hashed
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_register_user_without_name(self, session: Session):
        """Test user registration without name."""
        user_data = UserRegister(
            email="noname@example.com",
            password="secure_password_123"
        )

        user = AuthService.register_user(session, user_data)

        assert user is not None
        assert user.email == "noname@example.com"
        assert user.name is None

    def test_register_user_duplicate_email(self, session: Session, test_user: User):
        """Test registering with duplicate email."""
        user_data = UserRegister(
            email=test_user.email,  # Use existing user's email
            password="another_password",
            name="Another User"
        )

        user = AuthService.register_user(session, user_data)
        assert user is None  # Should return None for duplicate email

    def test_login_user_success(self, session: Session):
        """Test successful user login."""
        # First register a user
        password = "test_password_123"
        user_data = UserRegister(
            email="login@example.com",
            password=password,
            name="Login User"
        )
        registered_user = AuthService.register_user(session, user_data)

        # Now try to login
        logged_in_user = AuthService.login_user(session, "login@example.com", password)

        assert logged_in_user is not None
        assert logged_in_user.id == registered_user.id
        assert logged_in_user.email == "login@example.com"

    def test_login_user_wrong_password(self, session: Session):
        """Test login with wrong password."""
        # Register a user
        user_data = UserRegister(
            email="wrongpass@example.com",
            password="correct_password",
            name="User"
        )
        AuthService.register_user(session, user_data)

        # Try to login with wrong password
        logged_in_user = AuthService.login_user(session, "wrongpass@example.com", "wrong_password")
        assert logged_in_user is None

    def test_login_user_nonexistent_email(self, session: Session):
        """Test login with non-existent email."""
        logged_in_user = AuthService.login_user(session, "nonexistent@example.com", "any_password")
        assert logged_in_user is None

    def test_get_user_by_id_success(self, session: Session, test_user: User):
        """Test getting user by ID."""
        user = AuthService.get_user_by_id(session, test_user.id)

        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_user_by_id_not_found(self, session: Session):
        """Test getting non-existent user by ID."""
        user = AuthService.get_user_by_id(session, 99999)
        assert user is None

    def test_password_hashing_is_secure(self):
        """Test that same password produces different hashes (salt)."""
        password = "same_password"
        hash1 = AuthService.hash_password(password)
        hash2 = AuthService.hash_password(password)

        # Hashes should be different due to salt
        assert hash1 != hash2
        # But both should verify correctly
        assert AuthService.verify_password(password, hash1)
        assert AuthService.verify_password(password, hash2)

    def test_token_contains_user_data(self):
        """Test that token contains correct user data."""
        user_id = 42
        email = "user@example.com"
        data = {"sub": str(user_id), "email": email}

        token = AuthService.create_access_token(data)
        token_data = AuthService.verify_token(token)

        assert token_data is not None
        assert token_data.user_id == user_id
        assert token_data.email == email
