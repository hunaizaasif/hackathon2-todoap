"""Unit tests for TaskService."""
import pytest
from sqlmodel import Session
from src.models.user import User
from src.models.task import Task
from src.services.task_service import TaskService
from src.schemas.task import TaskCreate, TaskUpdate, TaskPatch


class TestTaskService:
    """Test suite for TaskService."""

    def test_create_task(self, session: Session, test_user: User):
        """Test creating a new task."""
        task_data = TaskCreate(
            title="Test Task",
            description="Test Description",
            status="pending"
        )

        task = TaskService.create_task(session, task_data, test_user.id)

        assert task.id is not None
        assert task.user_id == test_user.id
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.status == "pending"
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_create_task_without_description(self, session: Session, test_user: User):
        """Test creating a task without description."""
        task_data = TaskCreate(
            title="Task Without Description",
            status="pending"
        )

        task = TaskService.create_task(session, task_data, test_user.id)

        assert task.id is not None
        assert task.title == "Task Without Description"
        assert task.description is None
        assert task.status == "pending"

    def test_get_tasks_all(self, session: Session, test_user: User):
        """Test getting all tasks without filtering."""
        # Create multiple tasks
        for i in range(3):
            task_data = TaskCreate(title=f"Task {i}", status="pending")
            TaskService.create_task(session, task_data, test_user.id)

        tasks = TaskService.get_tasks(session)

        assert len(tasks) == 3

    def test_get_tasks_by_user_id(self, session: Session, test_user: User, test_user_2: User):
        """Test getting tasks filtered by user_id."""
        # Create tasks for user 1
        for i in range(2):
            task_data = TaskCreate(title=f"User1 Task {i}", status="pending")
            TaskService.create_task(session, task_data, test_user.id)

        # Create tasks for user 2
        for i in range(3):
            task_data = TaskCreate(title=f"User2 Task {i}", status="pending")
            TaskService.create_task(session, task_data, test_user_2.id)

        user1_tasks = TaskService.get_tasks(session, user_id=test_user.id)
        user2_tasks = TaskService.get_tasks(session, user_id=test_user_2.id)

        assert len(user1_tasks) == 2
        assert len(user2_tasks) == 3
        assert all(task.user_id == test_user.id for task in user1_tasks)
        assert all(task.user_id == test_user_2.id for task in user2_tasks)

    def test_get_task_by_id(self, session: Session, test_user: User):
        """Test getting a task by ID."""
        task_data = TaskCreate(title="Test Task", status="pending")
        created_task = TaskService.create_task(session, task_data, test_user.id)

        retrieved_task = TaskService.get_task_by_id(session, created_task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == "Test Task"

    def test_get_task_by_id_with_user_isolation(self, session: Session, test_user: User, test_user_2: User):
        """Test getting a task by ID with user isolation."""
        task_data = TaskCreate(title="User1 Task", status="pending")
        user1_task = TaskService.create_task(session, task_data, test_user.id)

        # User 1 can access their own task
        task = TaskService.get_task_by_id(session, user1_task.id, user_id=test_user.id)
        assert task is not None
        assert task.id == user1_task.id

        # User 2 cannot access user 1's task
        task = TaskService.get_task_by_id(session, user1_task.id, user_id=test_user_2.id)
        assert task is None

    def test_get_task_by_id_not_found(self, session: Session):
        """Test getting a non-existent task."""
        task = TaskService.get_task_by_id(session, 99999)
        assert task is None

    def test_update_task(self, session: Session, test_user: User):
        """Test updating a task (full update)."""
        import time

        task_data = TaskCreate(title="Original Title", description="Original", status="pending")
        created_task = TaskService.create_task(session, task_data, test_user.id)

        # Small delay to ensure updated_at will be different
        time.sleep(0.01)

        update_data = TaskUpdate(
            title="Updated Title",
            description="Updated Description",
            status="in_progress"
        )

        updated_task = TaskService.update_task(session, created_task.id, update_data)

        assert updated_task is not None
        assert updated_task.id == created_task.id
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.status == "in_progress"
        assert updated_task.updated_at >= created_task.updated_at

    def test_update_task_with_user_isolation(self, session: Session, test_user: User, test_user_2: User):
        """Test updating a task with user isolation."""
        task_data = TaskCreate(title="User1 Task", status="pending")
        user1_task = TaskService.create_task(session, task_data, test_user.id)

        update_data = TaskUpdate(title="Updated", description=None, status="complete")

        # User 2 cannot update user 1's task
        result = TaskService.update_task(session, user1_task.id, update_data, user_id=test_user_2.id)
        assert result is None

        # User 1 can update their own task
        result = TaskService.update_task(session, user1_task.id, update_data, user_id=test_user.id)
        assert result is not None
        assert result.title == "Updated"

    def test_patch_task(self, session: Session, test_user: User):
        """Test partially updating a task."""
        task_data = TaskCreate(title="Original", description="Description", status="pending")
        created_task = TaskService.create_task(session, task_data, test_user.id)

        # Only update status
        patch_data = TaskPatch(status="in_progress")

        patched_task = TaskService.patch_task(session, created_task.id, patch_data)

        assert patched_task is not None
        assert patched_task.title == "Original"  # Unchanged
        assert patched_task.description == "Description"  # Unchanged
        assert patched_task.status == "in_progress"  # Changed

    def test_patch_task_multiple_fields(self, session: Session, test_user: User):
        """Test patching multiple fields."""
        task_data = TaskCreate(title="Original", description="Original Desc", status="pending")
        created_task = TaskService.create_task(session, task_data, test_user.id)

        patch_data = TaskPatch(title="New Title", status="complete")

        patched_task = TaskService.patch_task(session, created_task.id, patch_data)

        assert patched_task is not None
        assert patched_task.title == "New Title"
        assert patched_task.description == "Original Desc"  # Unchanged
        assert patched_task.status == "complete"

    def test_patch_task_with_user_isolation(self, session: Session, test_user: User, test_user_2: User):
        """Test patching a task with user isolation."""
        task_data = TaskCreate(title="User1 Task", status="pending")
        user1_task = TaskService.create_task(session, task_data, test_user.id)

        patch_data = TaskPatch(status="complete")

        # User 2 cannot patch user 1's task
        result = TaskService.patch_task(session, user1_task.id, patch_data, user_id=test_user_2.id)
        assert result is None

    def test_delete_task(self, session: Session, test_user: User):
        """Test deleting a task."""
        task_data = TaskCreate(title="To Delete", status="pending")
        created_task = TaskService.create_task(session, task_data, test_user.id)

        # Delete the task
        result = TaskService.delete_task(session, created_task.id)
        assert result is True

        # Verify task is deleted
        deleted_task = TaskService.get_task_by_id(session, created_task.id)
        assert deleted_task is None

    def test_delete_task_with_user_isolation(self, session: Session, test_user: User, test_user_2: User):
        """Test deleting a task with user isolation."""
        task_data = TaskCreate(title="User1 Task", status="pending")
        user1_task = TaskService.create_task(session, task_data, test_user.id)

        # User 2 cannot delete user 1's task
        result = TaskService.delete_task(session, user1_task.id, user_id=test_user_2.id)
        assert result is False

        # Verify task still exists
        task = TaskService.get_task_by_id(session, user1_task.id)
        assert task is not None

        # User 1 can delete their own task
        result = TaskService.delete_task(session, user1_task.id, user_id=test_user.id)
        assert result is True

    def test_delete_nonexistent_task(self, session: Session):
        """Test deleting a non-existent task."""
        result = TaskService.delete_task(session, 99999)
        assert result is False
