"""Unit tests for validators."""

import pytest

from src.utils.validators import (
    TaskNotFoundError,
    ValidationError,
    validate_description,
    validate_task_id,
)


def test_validate_task_id_valid():
    """Test validating valid task ID."""
    assert validate_task_id("1") == 1
    assert validate_task_id("42") == 42
    assert validate_task_id("999") == 999


def test_validate_task_id_invalid_format():
    """Test validating invalid task ID format."""
    with pytest.raises(ValidationError, match="positive integer"):
        validate_task_id("abc")

    with pytest.raises(ValidationError, match="positive integer"):
        validate_task_id("1.5")

    with pytest.raises(ValidationError, match="positive integer"):
        validate_task_id("")


def test_validate_task_id_negative():
    """Test validating negative task ID."""
    with pytest.raises(ValidationError, match="positive integer"):
        validate_task_id("0")

    with pytest.raises(ValidationError, match="positive integer"):
        validate_task_id("-1")


def test_validate_description_valid():
    """Test validating valid description."""
    validate_description("Valid description")  # Should not raise
    validate_description("a" * 500)  # Exactly 500 chars should be valid


def test_validate_description_empty():
    """Test validating empty description."""
    with pytest.raises(ValidationError, match="cannot be empty"):
        validate_description("")

    with pytest.raises(ValidationError, match="cannot be empty"):
        validate_description("   ")


def test_validate_description_too_long():
    """Test validating too long description."""
    with pytest.raises(ValidationError, match="cannot exceed 500 characters"):
        validate_description("a" * 501)


def test_task_not_found_error():
    """Test TaskNotFoundError exception."""
    error = TaskNotFoundError(42)
    assert error.task_id == 42
    assert "42" in str(error)
    assert "not found" in str(error)
