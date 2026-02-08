# Phase 2: Todo Full-Stack Web Application

A persistent, multi-user Todo API built with FastAPI, SQLModel, and PostgreSQL with JWT authentication.

## Features

- RESTful CRUD API for task management
- JWT-based user authentication with bcrypt password hashing
- PostgreSQL database with SQLModel ORM
- User isolation (users can only access their own tasks)
- Data persistence across application restarts
- Comprehensive error handling and request logging
- Full test coverage with unit and integration tests

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Database**: Neon Serverless PostgreSQL (SQLite for local development)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Package Manager**: UV
- **Python**: 3.13+
- **Testing**: pytest, httpx

## Setup

### Prerequisites

- Python 3.13+
- UV package manager ([installation guide](https://github.com/astral-sh/uv))
- Neon PostgreSQL account (or use SQLite for local development)

### Installation

1. **Install dependencies:**
```bash
cd phase-2
uv sync
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your actual database credentials
```

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string (or `sqlite:///./test.db` for local)
- `AUTH_SECRET_KEY`: Secret key for JWT token signing (generate with `openssl rand -hex 32`)
- `APP_NAME`: Application name (default: "Phase 2 Todo API")
- `DEBUG`: Debug mode (default: false)
- `CORS_ORIGINS`: Comma-separated list of allowed origins (default: "*")

3. **Run database migrations:**
```bash
uv run alembic upgrade head
```

4. **Start the server:**
```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs (interactive API documentation)
- **ReDoc**: http://localhost:8000/redoc (alternative documentation)
- **Health Check**: http://localhost:8000/health

## API Usage

### Authentication Flow

#### 1. Register a new user
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password_123",
    "name": "John Doe"
  }'
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2026-02-05T19:00:00Z",
  "updated_at": "2026-02-05T19:00:00Z"
}
```

#### 2. Login to get access token
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=secure_password_123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Get current user info
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Task Management

All task endpoints require authentication. Include the JWT token in the Authorization header.

#### Create a task
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API docs",
    "status": "pending"
  }'
```

#### Get all tasks (for authenticated user)
```bash
curl -X GET http://localhost:8000/tasks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Get a specific task
```bash
curl -X GET http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Update a task (full update)
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated title",
    "description": "Updated description",
    "status": "in_progress"
  }'
```

#### Partially update a task
```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "complete"
  }'
```

#### Delete a task
```bash
curl -X DELETE http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Testing

### Run all tests
```bash
uv run pytest
```

### Run with verbose output
```bash
uv run pytest -v
```

### Run specific test file
```bash
uv run pytest tests/unit/test_task_service.py -v
```

### Run with coverage report
```bash
uv run pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### Test categories
- **Unit tests**: `tests/unit/` - Test individual service methods
- **Integration tests**: `tests/integration/` - Test API endpoints end-to-end

## Project Structure

```
phase-2/
├── src/
│   ├── main.py              # FastAPI app entry point with middleware
│   ├── config.py            # Pydantic Settings configuration
│   ├── database.py          # Database engine and connection pooling
│   ├── models/              # SQLModel entities
│   │   ├── user.py          # User model
│   │   └── task.py          # Task model with composite index
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── user.py          # User schemas (Register, Login, Response, Token)
│   │   └── task.py          # Task schemas (Create, Update, Patch, Response)
│   ├── api/                 # API route handlers
│   │   ├── deps.py          # Dependency injection (get_db, get_current_user)
│   │   ├── auth.py          # Authentication endpoints
│   │   └── tasks.py         # Task CRUD endpoints
│   └── services/            # Business logic layer
│       ├── auth_service.py  # Authentication service (JWT, bcrypt)
│       └── task_service.py  # Task service with user isolation
├── tests/
│   ├── conftest.py          # Pytest fixtures (test DB, test users)
│   ├── unit/                # Unit tests
│   │   ├── test_auth_service.py  # Auth service tests (17 tests)
│   │   └── test_task_service.py  # Task service tests (15 tests)
│   └── integration/         # Integration tests (optional)
├── alembic/                 # Database migrations
│   ├── env.py               # Alembic configuration
│   └── versions/            # Migration files
├── .env.example             # Example environment variables
├── alembic.ini              # Alembic configuration
├── pyproject.toml           # UV project configuration
└── README.md                # This file
```

## Database Migrations

### Create a new migration
```bash
uv run alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
uv run alembic upgrade head
```

### Rollback last migration
```bash
uv run alembic downgrade -1
```

### View migration history
```bash
uv run alembic history
```

## Development

### Code Quality
- All endpoints have comprehensive docstrings
- Type hints throughout the codebase
- Pydantic validation for all inputs
- SQLModel for type-safe database operations

### Security Features
- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens with 30-minute expiration
- User isolation enforced at service layer
- SQL injection prevention via SQLModel parameterization
- CORS middleware configured

### Error Handling
- Global exception handlers for database errors
- Validation error responses with detailed messages
- Request logging with processing time tracking
- Structured error responses with error types

## Troubleshooting

### Database connection issues
- Verify `DATABASE_URL` in `.env` is correct
- For Neon PostgreSQL, ensure connection pooling settings are appropriate
- For local development, use SQLite: `DATABASE_URL=sqlite:///./test.db`

### Authentication errors
- Ensure `AUTH_SECRET_KEY` is set in `.env`
- JWT tokens expire after 30 minutes - obtain a new token via `/auth/login`
- Check that Authorization header format is: `Bearer YOUR_TOKEN`

### Migration errors
- If "Target database is not up to date", run `uv run alembic upgrade head`
- If migration conflicts occur, check `alembic/versions/` for duplicate revisions

### Test failures
- Ensure test database is clean: `rm test.db` before running tests
- Install test dependencies: `uv sync --dev`
- Check that all required packages are installed: `uv run pip list`

## Production Deployment

### Environment Configuration
1. Set strong `AUTH_SECRET_KEY` (32+ random bytes)
2. Use production PostgreSQL database
3. Set `DEBUG=false`
4. Configure specific `CORS_ORIGINS` (not "*")
5. Use environment-specific `.env` files

### Running in Production
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or with Gunicorn:
```bash
uv run gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Project Specification](../specs/002-web-api-persistence/spec.md)
- [Implementation Plan](../specs/002-web-api-persistence/plan.md)
- [Task List](../specs/002-web-api-persistence/tasks.md)

## License

This project is part of the Hackathon-2 repository.
