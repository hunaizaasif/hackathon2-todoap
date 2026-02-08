# Phase 0: Research & Technology Decisions

**Feature**: Phase 2 - Todo Full-Stack Web Application
**Date**: 2026-02-05
**Status**: Complete

## Overview

This document captures research findings, technology decisions, and best practices for implementing Phase 2's Web API with persistence. All decisions align with the feature specification and constitution principles.

---

## 1. FastAPI Project Structure

### Decision
Use layered architecture with separation of concerns: models (database), schemas (API contracts), api (routes), and services (business logic).

### Rationale
- **Maintainability**: Clear separation makes code easier to understand and modify
- **Testability**: Business logic in services can be tested independently of HTTP layer
- **Scalability**: Structure supports growth from simple CRUD to complex business logic
- **FastAPI conventions**: Aligns with official FastAPI documentation patterns

### Alternatives Considered
- **Flat structure**: All code in single module - rejected due to poor scalability
- **Domain-driven design**: Feature-based modules - rejected as overkill for Phase 2 scope
- **Repository pattern**: Additional abstraction layer - rejected to avoid over-engineering

### Implementation Pattern
```python
# models/task.py - SQLModel entities (database)
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str = Field(max_length=200)
    # ...

# schemas/task.py - Pydantic schemas (API contracts)
class TaskCreate(BaseModel):
    title: str = Field(max_length=200)
    description: Optional[str] = Field(max_length=2000)
    # ...

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    # ...

# services/task_service.py - Business logic
class TaskService:
    def create_task(self, db: Session, task_data: TaskCreate, user_id: int) -> Task:
        # Business logic here
        pass

# api/tasks.py - HTTP routes
@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Route handler delegates to service
    pass
```

---

## 2. SQLModel vs SQLAlchemy Core

### Decision
Use SQLModel for ORM with SQLAlchemy Core for complex queries if needed.

### Rationale
- **Type safety**: SQLModel provides full Pydantic integration with type hints
- **Simplicity**: Single class definition for both database model and API schema
- **FastAPI integration**: Built by same author (Sebastián Ramírez), seamless integration
- **Validation**: Automatic request/response validation using Pydantic
- **Flexibility**: Can drop down to SQLAlchemy Core for complex queries

### Alternatives Considered
- **Pure SQLAlchemy**: More mature but requires separate Pydantic models - rejected for duplication
- **Tortoise ORM**: Async-first but less mature ecosystem - rejected for stability concerns
- **Raw SQL**: Maximum control but no type safety - rejected for maintainability

### Implementation Pattern
```python
from sqlmodel import SQLModel, Field, Session, select

# Single model serves both database and API
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200, min_length=1)
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Query with type safety
def get_user_tasks(db: Session, user_id: int) -> List[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    return db.exec(statement).all()
```

---

## 3. Neon Serverless PostgreSQL Connection Management

### Decision
Use connection pooling with SQLAlchemy engine, configure for serverless cold starts, implement retry logic.

### Rationale
- **Cold start handling**: Neon may have initial connection latency, pooling mitigates this
- **Connection limits**: Serverless databases have connection limits, pooling prevents exhaustion
- **Performance**: Reusing connections reduces overhead
- **Reliability**: Retry logic handles transient network issues

### Alternatives Considered
- **No pooling**: Simple but poor performance - rejected for production readiness
- **External pooler (PgBouncer)**: Additional infrastructure - rejected for Phase 2 simplicity
- **Async connections**: Better concurrency but adds complexity - deferred to future phases

### Implementation Pattern
```python
from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool

# Connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,              # Max connections in pool
    max_overflow=10,          # Additional connections if pool exhausted
    pool_pre_ping=True,       # Verify connections before use
    pool_recycle=3600,        # Recycle connections after 1 hour
    echo=False,               # Set True for SQL logging in dev
)

# Dependency for route handlers
def get_db():
    with Session(engine) as session:
        yield session
```

---

## 4. Better Auth Integration Strategy

### Decision
Research Better Auth documentation during implementation; use session-based authentication with middleware for protected routes.

### Rationale
- **Specification requirement**: Better Auth is mandated in Phase 2 spec
- **Session management**: Better Auth handles token generation and validation
- **Security**: Delegating auth to specialized library reduces security risks
- **Integration point**: FastAPI middleware can intercept requests and validate sessions

### Alternatives Considered
- **Custom JWT implementation**: Full control but high security risk - rejected per spec
- **OAuth providers only**: Simpler but doesn't support email/password - rejected per spec
- **Passport.js**: Node.js library, not Python - not applicable

### Implementation Pattern (Conceptual)
```python
# Exact implementation depends on Better Auth Python SDK
from fastapi import Depends, HTTPException
from better_auth import verify_session  # Hypothetical import

# Dependency to get current user from session
async def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Verify session with Better Auth
    user_id = await verify_session(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")

    # Fetch user from database
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# Protected route
@router.get("/tasks")
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Automatically filtered to current user
    return task_service.get_user_tasks(db, current_user.id)
```

**Note**: Better Auth integration details will be finalized during implementation based on official documentation.

---

## 5. Database Migration Strategy

### Decision
Use Alembic for database migrations with auto-generation from SQLModel models.

### Rationale
- **Version control**: Migrations tracked in git, reproducible across environments
- **Team collaboration**: Multiple developers can evolve schema safely
- **Rollback capability**: Can revert schema changes if needed
- **SQLAlchemy integration**: Alembic is the standard migration tool for SQLAlchemy/SQLModel
- **Auto-generation**: Can generate migrations from model changes

### Alternatives Considered
- **Manual SQL scripts**: Full control but error-prone - rejected for safety
- **SQLModel.metadata.create_all()**: Simple but no versioning - rejected for production readiness
- **Django-style migrations**: Not available for FastAPI - not applicable

### Implementation Pattern
```bash
# Initialize Alembic
alembic init alembic

# Generate migration from models
alembic revision --autogenerate -m "Create tasks and users tables"

# Apply migrations
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

```python
# alembic/env.py configuration
from sqlmodel import SQLModel
from src.models.task import Task
from src.models.user import User

target_metadata = SQLModel.metadata

# Alembic will detect changes to SQLModel models
```

---

## 6. Testing Strategy for FastAPI

### Decision
Use pytest with TestClient for integration tests, separate test database, fixtures for common setup.

### Rationale
- **FastAPI support**: TestClient provides synchronous testing interface
- **Isolation**: Separate test database prevents pollution of dev data
- **Fixtures**: Reusable setup code (test DB, authenticated users, sample data)
- **Coverage**: Integration tests verify full request/response cycle
- **Speed**: In-memory SQLite for fast test execution

### Alternatives Considered
- **Manual testing only**: Fast initially but not sustainable - rejected for quality
- **Postman collections**: Good for manual testing but not automated - supplementary only
- **Unit tests only**: Fast but don't catch integration issues - use both unit and integration

### Implementation Pattern
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from src.main import app
from src.database import get_db

# In-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_test_db():
        yield session
    app.dependency_overrides[get_db] = get_test_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# tests/integration/test_tasks_api.py
def test_create_task(client: TestClient):
    response = client.post("/tasks", json={
        "title": "Test task",
        "description": "Test description"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert "id" in data
```

---

## 7. User Isolation Implementation

### Decision
Implement user isolation at the service layer with automatic filtering based on authenticated user, enforce at database query level.

### Rationale
- **Security**: Prevents accidental exposure of other users' data
- **Consistency**: All queries automatically filtered, no manual filtering needed
- **Performance**: Database-level filtering is efficient with proper indexes
- **Simplicity**: Service layer handles isolation, routes just pass current user

### Alternatives Considered
- **Application-level filtering**: Filter after fetching all data - rejected for performance and security
- **Database views**: Per-user views - rejected for complexity and scalability
- **Row-level security (RLS)**: PostgreSQL feature - deferred as overkill for Phase 2

### Implementation Pattern
```python
# services/task_service.py
class TaskService:
    def get_user_tasks(self, db: Session, user_id: int) -> List[Task]:
        """Get all tasks for a specific user."""
        statement = select(Task).where(Task.user_id == user_id)
        return db.exec(statement).all()

    def get_task_by_id(self, db: Session, task_id: int, user_id: int) -> Optional[Task]:
        """Get a specific task, ensuring it belongs to the user."""
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # Isolation enforced here
        )
        return db.exec(statement).first()

    def update_task(self, db: Session, task_id: int, user_id: int, updates: dict) -> Optional[Task]:
        """Update a task, ensuring it belongs to the user."""
        task = self.get_task_by_id(db, task_id, user_id)
        if not task:
            return None  # Either doesn't exist or doesn't belong to user

        for key, value in updates.items():
            setattr(task, key, value)
        task.updated_at = datetime.utcnow()
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

# api/tasks.py
@router.get("/tasks/{task_id}")
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = task_service.get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

**Security Note**: Always pass `user_id` to service methods and filter at query level. Never trust client-provided user_id without authentication.

---

## 8. Error Handling and Validation

### Decision
Use Pydantic for request validation, FastAPI exception handlers for consistent error responses, custom exceptions for business logic errors.

### Rationale
- **Automatic validation**: Pydantic validates requests before reaching route handlers
- **Consistent responses**: Exception handlers ensure uniform error format
- **HTTP semantics**: Proper status codes (400, 401, 403, 404, 500)
- **Client-friendly**: Detailed error messages help API consumers debug issues

### Alternatives Considered
- **Manual validation**: Full control but repetitive - rejected for maintainability
- **Try-except everywhere**: Verbose and inconsistent - rejected for code quality
- **Generic error responses**: Simple but poor developer experience - rejected for usability

### Implementation Pattern
```python
# Custom exceptions
class TaskNotFoundError(Exception):
    pass

class UnauthorizedAccessError(Exception):
    pass

# Exception handlers
@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": "Task not found"}
    )

@app.exception_handler(UnauthorizedAccessError)
async def unauthorized_access_handler(request: Request, exc: UnauthorizedAccessError):
    return JSONResponse(
        status_code=403,
        content={"detail": "You do not have permission to access this resource"}
    )

# Pydantic validation
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(max_length=2000, default=None)
    status: Literal["pending", "in_progress", "complete"] = "pending"

    @validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip()

# Usage in routes
@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,  # Automatically validated by Pydantic
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # If we reach here, task is valid
    return task_service.create_task(db, task, current_user.id)
```

---

## 9. Environment Configuration

### Decision
Use Pydantic Settings for environment variable management with `.env` file support and validation.

### Rationale
- **Type safety**: Environment variables validated and typed
- **Documentation**: Settings class serves as documentation of required config
- **Defaults**: Can provide sensible defaults for development
- **Security**: Sensitive values (DB passwords, auth secrets) never hardcoded

### Implementation Pattern
```python
# src/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str

    # Better Auth
    auth_secret_key: str
    auth_api_url: str

    # Application
    app_name: str = "Phase 2 Todo API"
    debug: bool = False
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# .env.example (checked into git)
DATABASE_URL=postgresql://user:pass@localhost/dbname
AUTH_SECRET_KEY=your-secret-key-here
AUTH_API_URL=https://auth.example.com
DEBUG=true
CORS_ORIGINS=["http://localhost:3000"]

# .env (NOT checked into git, user creates from example)
DATABASE_URL=postgresql://real-user:real-pass@neon.tech/real-db
AUTH_SECRET_KEY=actual-secret-key
AUTH_API_URL=https://auth.production.com
DEBUG=false
```

---

## 10. API Response Format

### Decision
Use consistent JSON response format with proper HTTP status codes, Pydantic response models for type safety.

### Rationale
- **Predictability**: Clients know what to expect from all endpoints
- **Type safety**: Response models prevent accidental data leaks
- **Documentation**: FastAPI auto-generates OpenAPI docs from response models
- **Validation**: Responses validated before sending to client

### Implementation Pattern
```python
# Success responses use Pydantic models
class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allow creation from ORM models

# Error responses use consistent format
{
    "detail": "Error message here"
}

# Or for validation errors (automatic from FastAPI)
{
    "detail": [
        {
            "loc": ["body", "title"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}

# List responses
class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int

# Route with response model
@router.get("/tasks", response_model=TaskListResponse)
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = task_service.get_user_tasks(db, current_user.id)
    return TaskListResponse(tasks=tasks, total=len(tasks))
```

---

## Summary of Key Decisions

| Area | Decision | Primary Rationale |
|------|----------|-------------------|
| Architecture | Layered (models/schemas/api/services) | Separation of concerns, testability |
| ORM | SQLModel | Type safety, Pydantic integration |
| Database | Neon PostgreSQL with connection pooling | Serverless optimization, reliability |
| Authentication | Better Auth with session middleware | Spec requirement, security |
| Migrations | Alembic with auto-generation | Version control, team collaboration |
| Testing | pytest + TestClient + fixtures | FastAPI support, isolation |
| User Isolation | Service-layer filtering with user_id | Security, consistency |
| Validation | Pydantic models | Automatic, type-safe |
| Configuration | Pydantic Settings | Type safety, validation |
| Error Handling | Exception handlers + HTTP status codes | Consistency, client-friendly |

---

## Open Questions for Implementation

1. **Better Auth SDK**: Exact Python SDK and integration pattern (to be determined from documentation)
2. **Database migrations**: Initial schema creation strategy (Alembic vs SQLModel.metadata.create_all for first run)
3. **CORS configuration**: Specific origins for development vs production
4. **Logging strategy**: Structured logging format and log levels
5. **Health check endpoint**: Include database connectivity check?

These will be resolved during Phase 1 (Design & Contracts) and implementation.

---

**Research Status**: ✅ Complete
**Next Phase**: Phase 1 - Design & Contracts (data-model.md, contracts/, quickstart.md)
