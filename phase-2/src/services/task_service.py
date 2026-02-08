"""Task service for business logic."""
from sqlmodel import Session, select
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate, TaskPatch
from datetime import datetime
from typing import List, Optional


class TaskService:
    """Service class for task operations."""

    @staticmethod
    def create_task(db: Session, task_data: TaskCreate, user_id: int) -> Task:
        """Create a new task.

        Args:
            db: Database session
            task_data: Task creation data
            user_id: ID of the user creating the task

        Returns:
            Task: Created task
        """
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_tasks(db: Session, user_id: Optional[int] = None) -> List[Task]:
        """Get all tasks, optionally filtered by user_id.

        Args:
            db: Database session
            user_id: Optional user ID to filter tasks

        Returns:
            List[Task]: List of tasks
        """
        statement = select(Task)
        if user_id is not None:
            statement = statement.where(Task.user_id == user_id)
        tasks = db.exec(statement).all()
        return list(tasks)

    @staticmethod
    def get_task_by_id(db: Session, task_id: int, user_id: Optional[int] = None) -> Optional[Task]:
        """Get a task by ID, optionally ensuring it belongs to the user.

        Args:
            db: Database session
            task_id: Task ID
            user_id: Optional user ID for isolation

        Returns:
            Optional[Task]: Task if found and belongs to user, None otherwise
        """
        statement = select(Task).where(Task.id == task_id)
        if user_id is not None:
            statement = statement.where(Task.user_id == user_id)
        return db.exec(statement).first()

    @staticmethod
    def update_task(db: Session, task_id: int, task_data: TaskUpdate, user_id: Optional[int] = None) -> Optional[Task]:
        """Update a task (full update), optionally ensuring it belongs to the user.

        Args:
            db: Database session
            task_id: Task ID
            task_data: Task update data
            user_id: Optional user ID for isolation

        Returns:
            Optional[Task]: Updated task if found and belongs to user, None otherwise
        """
        task = TaskService.get_task_by_id(db, task_id, user_id)
        if not task:
            return None

        task.title = task_data.title
        task.description = task_data.description
        task.status = task_data.status
        task.updated_at = datetime.utcnow()

        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def patch_task(db: Session, task_id: int, task_data: TaskPatch, user_id: Optional[int] = None) -> Optional[Task]:
        """Partially update a task, optionally ensuring it belongs to the user.

        Args:
            db: Database session
            task_id: Task ID
            task_data: Task patch data
            user_id: Optional user ID for isolation

        Returns:
            Optional[Task]: Updated task if found and belongs to user, None otherwise
        """
        task = TaskService.get_task_by_id(db, task_id, user_id)
        if not task:
            return None

        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.status is not None:
            task.status = task_data.status

        task.updated_at = datetime.utcnow()

        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int, user_id: Optional[int] = None) -> bool:
        """Delete a task, optionally ensuring it belongs to the user.

        Args:
            db: Database session
            task_id: Task ID
            user_id: Optional user ID for isolation

        Returns:
            bool: True if deleted, False if not found or doesn't belong to user
        """
        task = TaskService.get_task_by_id(db, task_id, user_id)
        if not task:
            return False

        db.delete(task)
        db.commit()
        return True
