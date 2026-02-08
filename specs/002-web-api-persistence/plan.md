# Implementation Plan: Phase 2 - Todo Full-Stack Web Application

**Branch**: `002-web-api-persistence` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-web-api-persistence/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform Phase 1's in-memory CLI Todo application into a persistent, multi-user Web API using FastAPI, SQLModel ORM, Neon Serverless PostgreSQL, and Better Auth. The API will provide RESTful CRUD endpoints for task management with user isolation, authentication, and data persistence across application restarts.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI (web framework), SQLModel (ORM), Better Auth (authentication), Pydantic (validation)
**Storage**: Neon Serverless PostgreSQL (cloud-hosted PostgreSQL)
**Testing**: pytest (unit and integration tests), httpx (API testing client)
**Target Platform**: Linux server (development and production)
**Project Type**: Web API (backend only, no frontend)
**Performance Goals**: <500ms p95 latency for API requests under normal load
**Constraints**: Phase isolation (all code in /phase-2), no frontend UI, REST-only (no GraphQL)
**Scale/Scope**: Single-server deployment, ~10 API endpoints, 2 database tables (tasks, users)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Phase Isolation ✅
- All Phase 2 code will reside in `/phase-2/` directory
- Phase 1 CLI code in `/phase-1/` remains untouched
- No modifications to Phase 1 code
- Phase 2 is independent and can be developed/tested separately

### Principle II: Spec-Driven Development ✅
- Specification complete in `specs/002-web-api-persistence/spec.md`
- Planning in progress (this document)
- Tasks will be generated via `/sp.tasks` after planning
- Implementation will follow task execution via `/sp.implement`

### Principle III: Scope Discipline ✅
- All requirements align with Phase 2 definition in project document
- No Phase 3 features (AI agents, MCP) included
- No Phase 4 features (Docker, Kubernetes) included
- No Phase 5 features (Kafka, event-driven) included
- Out-of-scope items explicitly documented in spec

### Principle IV: Protected Directories ✅
- No modifications to `.specify/` directory
- No modifications to `.specifyplus/` or `.speckit/` (if present)
- All work contained in `/phase-2/` and `specs/002-web-api-persistence/`

### Principle V: Verification-First ✅
- Each user story includes explicit acceptance scenarios
- Success criteria defined with measurable outcomes
- Integration tests will be required for all API endpoints
- Phase completion requires validation of all acceptance criteria

### Principle VI: Evolutionary Architecture ✅
- Builds on Phase 1's domain logic (Task entity concept)
- Adds persistence layer without breaking Phase 1
- Adds web API layer as new interface
- Prepares foundation for Phase 3 AI integration
- Phase 1 CLI can coexist with Phase 2 API (different directories)

**GATE STATUS**: ✅ PASS - All constitution principles satisfied, no violations to justify

## Project Structure

### Documentation (this feature)

```text
specs/002-web-api-persistence/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology decisions and patterns)
├── data-model.md        # Phase 1 output (database schema and entities)
├── quickstart.md        # Phase 1 output (setup and usage guide)
├── contracts/           # Phase 1 output (API contracts)
│   └── openapi.yaml     # OpenAPI 3.0 specification
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase-2/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and environment variables
│   ├── database.py          # Database connection and session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task SQLModel entity
│   │   └── user.py          # User SQLModel entity (Better Auth integration)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py          # Pydantic request/response schemas for tasks
│   │   └── user.py          # Pydantic request/response schemas for users
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependency injection (DB session, auth)
│   │   ├── tasks.py         # Task CRUD endpoints
│   │   └── auth.py          # Authentication endpoints (Better Auth)
│   └── services/
│       ├── __init__.py
│       ├── task_service.py  # Business logic for task operations
│       └── auth_service.py  # Authentication business logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures (test DB, test client)
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_tasks_api.py      # Integration tests for task endpoints
│   │   └── test_auth_api.py       # Integration tests for auth endpoints
│   └── unit/
│       ├── __init__.py
│       ├── test_task_service.py   # Unit tests for task service
│       └── test_auth_service.py   # Unit tests for auth service
├── alembic/                 # Database migrations (if using Alembic)
│   ├── versions/
│   └── env.py
├── .env.example             # Example environment variables
├── pyproject.toml           # UV project configuration
├── README.md                # Phase 2 documentation
└── alembic.ini              # Alembic configuration (if using)
```

**Structure Decision**: Web application structure (backend only) selected because this is a REST API without frontend. The structure follows FastAPI best practices with clear separation between models (database), schemas (API contracts), api (routes), and services (business logic). All code is isolated in `/phase-2/` per constitution principle I.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All design decisions align with constitution principles:
- Phase isolation maintained (all code in `/phase-2/`)
- Scope discipline enforced (no Phase 3/4/5 features)
- Evolutionary architecture followed (builds on Phase 1 concepts)
- Verification-first approach (acceptance criteria defined)

---

## Phase 0: Research Summary

**Status**: ✅ Complete

**Artifacts Generated**:
- `research.md`: Technology decisions and implementation patterns

**Key Decisions**:
1. **Architecture**: Layered structure (models/schemas/api/services)
2. **ORM**: SQLModel for type safety and Pydantic integration
3. **Database**: Neon PostgreSQL with connection pooling
4. **Authentication**: Better Auth with session middleware
5. **Migrations**: Alembic with auto-generation
6. **Testing**: pytest with TestClient and fixtures
7. **User Isolation**: Service-layer filtering with user_id
8. **Validation**: Pydantic models for automatic validation
9. **Configuration**: Pydantic Settings for environment variables
10. **Error Handling**: Exception handlers with proper HTTP status codes

All decisions documented in `research.md` with rationale and alternatives considered.

---

## Phase 1: Design & Contracts Summary

**Status**: ✅ Complete

**Artifacts Generated**:
- `data-model.md`: Database schema with entities, relationships, and validation rules
- `contracts/openapi.yaml`: OpenAPI 3.0 specification with all endpoints
- `quickstart.md`: Setup and usage guide for developers

**Database Schema**:
- **User table**: id, email, password_hash, name, created_at, updated_at
- **Task table**: id, user_id, title, description, status, created_at, updated_at
- **Relationship**: User → Task (one-to-many via foreign key)
- **Indexes**: Optimized for user isolation queries

**API Endpoints**:
- `POST /auth/register`: User registration
- `POST /auth/login`: User authentication
- `POST /auth/logout`: Session invalidation
- `GET /tasks`: List user's tasks (with optional status filter)
- `POST /tasks`: Create new task
- `GET /tasks/{id}`: Get specific task
- `PUT /tasks/{id}`: Full update
- `PATCH /tasks/{id}`: Partial update
- `DELETE /tasks/{id}`: Delete task

**Agent Context Updated**: CLAUDE.md now includes Phase 2 technologies

---

## Constitution Check (Post-Design Re-evaluation)

*Re-checking all principles after design phase completion*

### Principle I: Phase Isolation ✅
- All Phase 2 code structure defined in `/phase-2/` directory
- No modifications to Phase 1 code required
- Clear separation maintained in project structure
- **Status**: PASS

### Principle II: Spec-Driven Development ✅
- Specification complete and approved
- Planning complete (this document)
- Design artifacts complete (research, data-model, contracts, quickstart)
- Ready for task generation via `/sp.tasks`
- **Status**: PASS

### Principle III: Scope Discipline ✅
- All endpoints align with Phase 2 requirements
- No AI features (Phase 3) included
- No containerization (Phase 4) included
- No event-driven patterns (Phase 5) included
- Out-of-scope items explicitly documented
- **Status**: PASS

### Principle IV: Protected Directories ✅
- No modifications to `.specify/` directory
- All artifacts in `specs/002-web-api-persistence/`
- Agent context update followed proper procedure
- **Status**: PASS

### Principle V: Verification-First ✅
- Each endpoint has defined request/response schemas
- Acceptance scenarios defined in spec.md
- Testing strategy documented in research.md
- Integration and unit test structure planned
- **Status**: PASS

### Principle VI: Evolutionary Architecture ✅
- Builds on Phase 1's Task entity concept
- Adds persistence without breaking Phase 1
- Prepares foundation for Phase 3 (AI agents will consume this API)
- Database schema supports future extensions
- **Status**: PASS

**FINAL GATE STATUS**: ✅ PASS - All constitution principles satisfied after design phase

---

## Next Steps

1. **Generate Tasks**: Run `/sp.tasks` to create dependency-ordered task breakdown
2. **Review Tasks**: Validate task list aligns with this plan
3. **Implement**: Run `/sp.implement` to execute tasks with verification
4. **Document Decisions**: Run `/sp.adr` for architecturally significant decisions
5. **Commit & PR**: Run `/sp.git.commit_pr` when implementation complete

---

## Planning Artifacts Summary

| Artifact | Path | Status | Description |
|----------|------|--------|-------------|
| Implementation Plan | `specs/002-web-api-persistence/plan.md` | ✅ Complete | This document |
| Research | `specs/002-web-api-persistence/research.md` | ✅ Complete | Technology decisions and patterns |
| Data Model | `specs/002-web-api-persistence/data-model.md` | ✅ Complete | Database schema and entities |
| API Contracts | `specs/002-web-api-persistence/contracts/openapi.yaml` | ✅ Complete | OpenAPI 3.0 specification |
| Quickstart Guide | `specs/002-web-api-persistence/quickstart.md` | ✅ Complete | Setup and usage instructions |
| Agent Context | `CLAUDE.md` | ✅ Updated | Added Phase 2 technologies |

---

**Planning Status**: ✅ COMPLETE
**Branch**: `002-web-api-persistence`
**Ready for**: Task generation (`/sp.tasks`)
