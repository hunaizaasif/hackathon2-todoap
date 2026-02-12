---
title: Phase 2 Todo API
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# Phase 2 Todo API

A persistent, multi-user Todo API built with FastAPI, SQLModel, and PostgreSQL.

## Features

- ✅ User authentication with JWT tokens
- ✅ CRUD operations for tasks
- ✅ Multi-user support with user isolation
- ✅ PostgreSQL database with SQLModel ORM
- ✅ Database migrations with Alembic
- ✅ Comprehensive error handling
- ✅ Request logging and monitoring

## API Documentation

Once deployed, visit `/docs` for interactive API documentation (Swagger UI).

## Environment Variables

Configure these in your Hugging Face Space settings:

```
DATABASE_URL=postgresql://user:password@host:port/database
AUTH_SECRET_KEY=your-secret-key-here
DEBUG=false
```

## Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /tasks` - List all tasks (authenticated)
- `POST /tasks` - Create new task (authenticated)
- `GET /tasks/{id}` - Get task by ID (authenticated)
- `PUT /tasks/{id}` - Update task (authenticated)
- `DELETE /tasks/{id}` - Delete task (authenticated)

## Tech Stack

- FastAPI
- SQLModel
- PostgreSQL (Neon Serverless)
- Alembic
- Pydantic
- Python 3.13+
