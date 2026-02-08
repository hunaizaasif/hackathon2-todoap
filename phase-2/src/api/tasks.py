"""Task API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from src.api.deps import get_db, get_current_user
from src.models.user import User
from src.schemas.task import TaskCreate, TaskUpdate, TaskPatch, TaskResponse
from src.services.task_service import TaskService


router = APIRouter(prefix="/tasks", tags=["Tasks"])
task_service = TaskService()


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task for the authenticated user.

    Args:
        task: Task creation data
        current_user: Authenticated user
        db: Database session

    Returns:
        TaskResponse: Created task

    Raises:
        HTTPException: 400 if validation fails, 401 if not authenticated
    """
    try:
        created_task = task_service.create_task(db, task, current_user.id)
        return created_task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all tasks for the authenticated user.

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        List[TaskResponse]: List of user's tasks

    Raises:
        HTTPException: 401 if not authenticated
    """
    tasks = task_service.get_tasks(db, user_id=current_user.id)
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task by ID for the authenticated user.

    Args:
        task_id: Task ID
        current_user: Authenticated user
        db: Database session

    Returns:
        TaskResponse: Task details

    Raises:
        HTTPException: 404 if task not found or doesn't belong to user, 401 if not authenticated
    """
    task = task_service.get_task_by_id(db, task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a task (full update) for the authenticated user.

    Args:
        task_id: Task ID
        task: Task update data
        current_user: Authenticated user
        db: Database session

    Returns:
        TaskResponse: Updated task

    Raises:
        HTTPException: 404 if task not found or doesn't belong to user, 400 if validation fails, 401 if not authenticated
    """
    try:
        updated_task = task_service.update_task(db, task_id, task, user_id=current_user.id)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(
    task_id: int,
    task: TaskPatch,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Partially update a task for the authenticated user.

    Args:
        task_id: Task ID
        task: Task patch data
        current_user: Authenticated user
        db: Database session

    Returns:
        TaskResponse: Updated task

    Raises:
        HTTPException: 404 if task not found or doesn't belong to user, 400 if validation fails, 401 if not authenticated
    """
    try:
        updated_task = task_service.patch_task(db, task_id, task, user_id=current_user.id)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task for the authenticated user.

    Args:
        task_id: Task ID
        current_user: Authenticated user
        db: Database session

    Raises:
        HTTPException: 404 if task not found or doesn't belong to user, 401 if not authenticated
    """
    deleted = task_service.delete_task(db, task_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
