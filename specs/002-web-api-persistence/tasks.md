# Tasks: Phase 2 - Todo Full-Stack Web Application

**Input**: Design documents from `/specs/002-web-api-persistence/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Tests**: Integration tests are included as optional tasks. They can be implemented alongside or after the corresponding features.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

All code resides in `/phase-2/` directory per constitution principle I (Phase Isolation).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create phase-2 directory structure per plan.md (src/, tests/, alembic/)
- [x] T002 Initialize UV project with pyproject.toml in phase-2/
- [x] T003 [P] Create .env.example file with required environment variables in phase-2/
- [x] T004 [P] Create phase-2/README.md with setup instructions
- [x] T005 [P] Create .gitignore for Python/FastAPI project in phase-2/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Install core dependencies: fastapi, uvicorn, sqlmodel, psycopg2-binary, alembic, pydantic-settings
- [x] T007 Create phase-2/src/config.py with Pydantic Settings for environment configuration
- [x] T008 Create phase-2/src/database.py with SQLAlchemy engine and session management
- [x] T009 [P] Create phase-2/src/models/__init__.py (empty module file)
- [x] T010 [P] Create phase-2/src/schemas/__init__.py (empty module file)
- [x] T011 [P] Create phase-2/src/api/__init__.py (empty module file)
- [x] T012 [P] Create phase-2/src/services/__init__.py (empty module file)
- [x] T013 Create phase-2/src/models/user.py with User SQLModel entity per data-model.md
- [x] T014 Create phase-2/src/models/task.py with Task SQLModel entity per data-model.md
- [x] T015 Initialize Alembic in phase-2/ with `alembic init alembic`
- [x] T016 Configure phase-2/alembic/env.py to import SQLModel metadata from models
- [x] T017 Generate initial migration for User and Task tables with Alembic
- [x] T018 Create phase-2/src/main.py with FastAPI app initialization and CORS configuration
- [x] T019 Create phase-2/src/api/deps.py with get_db dependency for database sessions
- [x] T020 Add health check endpoint GET /health in phase-2/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Retrieve Tasks via API (Priority: P1) 🎯 MVP

**Goal**: API consumers can create new tasks and retrieve all tasks through REST endpoints, with data persisting across application restarts.

**Independent Test**: Make POST requests to create tasks and GET requests to retrieve them. Restart the server and verify tasks still exist.

### Implementation for User Story 1

- [x] T021 [P] [US1] Create phase-2/src/schemas/task.py with TaskCreate, TaskUpdate, TaskResponse Pydantic schemas
- [x] T022 [US1] Create phase-2/src/services/task_service.py with create_task and get_tasks methods
- [x] T023 [US1] Create phase-2/src/api/tasks.py with APIRouter for task endpoints
- [x] T024 [US1] Implement POST /tasks endpoint in phase-2/src/api/tasks.py (creates task with user_id in request body)
- [x] T025 [US1] Implement GET /tasks endpoint in phase-2/src/api/tasks.py (retrieves all tasks, optional user_id filter)
- [x] T026 [US1] Implement GET /tasks/{id} endpoint in phase-2/src/api/tasks.py (retrieves specific task)
- [x] T027 [US1] Add task router to FastAPI app in phase-2/src/main.py
- [x] T028 [US1] Add validation for task title (1-200 chars, non-empty) in TaskCreate schema
- [x] T029 [US1] Add validation for task description (max 2000 chars) in TaskCreate schema
- [x] T030 [US1] Add validation for task status (enum: pending, in_progress, complete) in TaskCreate schema
- [x] T031 [US1] Add error handling for 404 Not Found when task doesn't exist in GET /tasks/{id}
- [x] T032 [US1] Add error handling for 400 Bad Request for validation errors in POST /tasks

### Integration Tests for User Story 1 (Optional)

- [ ] T033 [P] [US1] Create phase-2/tests/conftest.py with pytest fixtures (test database, test client)
- [ ] T034 [P] [US1] Create phase-2/tests/integration/test_tasks_api.py
- [ ] T035 [US1] Write integration test for POST /tasks with valid data (expects 201 Created)
- [ ] T036 [US1] Write integration test for GET /tasks (expects 200 OK with array)
- [ ] T037 [US1] Write integration test for GET /tasks/{id} with existing task (expects 200 OK)
- [ ] T038 [US1] Write integration test for GET /tasks/{id} with non-existent task (expects 404 Not Found)
- [ ] T039 [US1] Write integration test for POST /tasks with missing required fields (expects 400 Bad Request)
- [ ] T040 [US1] Write integration test for data persistence across server restarts

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Tasks can be created, retrieved, and persist in the database.

---

## Phase 4: User Story 2 - Update and Delete Tasks via API (Priority: P2)

**Goal**: API consumers can modify existing task details and permanently remove tasks they no longer need.

**Independent Test**: Create a task via POST, update it via PUT/PATCH, verify changes via GET, delete it via DELETE, and confirm it's gone with another GET.

### Implementation for User Story 2

- [x] T041 [P] [US2] Add TaskPatch schema to phase-2/src/schemas/task.py for partial updates
- [x] T042 [US2] Add update_task method to phase-2/src/services/task_service.py
- [x] T043 [US2] Add delete_task method to phase-2/src/services/task_service.py
- [x] T044 [US2] Implement PUT /tasks/{id} endpoint in phase-2/src/api/tasks.py (full update)
- [x] T045 [US2] Implement PATCH /tasks/{id} endpoint in phase-2/src/api/tasks.py (partial update)
- [x] T046 [US2] Implement DELETE /tasks/{id} endpoint in phase-2/src/api/tasks.py
- [x] T047 [US2] Add automatic updated_at timestamp update in update_task service method
- [x] T048 [US2] Add error handling for 404 Not Found in PUT /tasks/{id} when task doesn't exist
- [x] T049 [US2] Add error handling for 404 Not Found in PATCH /tasks/{id} when task doesn't exist
- [x] T050 [US2] Add error handling for 404 Not Found in DELETE /tasks/{id} when task doesn't exist
- [x] T051 [US2] Add validation for PUT /tasks/{id} to ensure all required fields are provided
- [x] T052 [US2] Add validation for PATCH /tasks/{id} to allow optional fields only

### Integration Tests for User Story 2 (Optional)

- [ ] T053 [P] [US2] Write integration test for PUT /tasks/{id} with valid data (expects 200 OK)
- [ ] T054 [P] [US2] Write integration test for PATCH /tasks/{id} with status change only (expects 200 OK)
- [ ] T055 [P] [US2] Write integration test for DELETE /tasks/{id} (expects 204 No Content)
- [ ] T056 [P] [US2] Write integration test for PUT /tasks/{id} with non-existent task (expects 404 Not Found)
- [ ] T057 [P] [US2] Write integration test for PUT /tasks/{id} with invalid data (expects 400 Bad Request)
- [ ] T058 [US2] Write integration test for DELETE /tasks/{id} followed by GET /tasks/{id} (expects 404)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Full CRUD operations are available for tasks.

---

## Phase 5: User Story 3 - User Isolation and Task Filtering (Priority: P3)

**Goal**: Each user can only see and manage their own tasks, with the system automatically filtering tasks based on the authenticated user's identity.

**Independent Test**: Create tasks with different user_id values. Query GET /tasks?user_id=1 and verify only tasks belonging to user 1 are returned. Attempt to update/delete a task belonging to a different user and verify appropriate access control.

### Implementation for User Story 3

- [x] T059 [US3] Add get_task_by_id method with user_id filtering to phase-2/src/services/task_service.py
- [x] T060 [US3] Update get_tasks method to filter by user_id in phase-2/src/services/task_service.py
- [x] T061 [US3] Update GET /tasks endpoint to support user_id query parameter in phase-2/src/api/tasks.py
- [x] T062 [US3] Update GET /tasks/{id} to verify task belongs to user_id in phase-2/src/api/tasks.py
- [x] T063 [US3] Update PUT /tasks/{id} to verify task belongs to user_id in phase-2/src/api/tasks.py
- [x] T064 [US3] Update PATCH /tasks/{id} to verify task belongs to user_id in phase-2/src/api/tasks.py
- [x] T065 [US3] Update DELETE /tasks/{id} to verify task belongs to user_id in phase-2/src/api/tasks.py
- [x] T066 [US3] Add error handling for 403 Forbidden when user attempts to access another user's task
- [x] T067 [US3] Add composite index (user_id, status) to Task model for optimized filtering
- [x] T068 [US3] Generate Alembic migration for composite index addition

### Integration Tests for User Story 3 (Optional)

- [ ] T069 [P] [US3] Write integration test for GET /tasks?user_id=1 filtering (expects only user 1 tasks)
- [ ] T070 [P] [US3] Write integration test for GET /tasks?user_id=3 with no tasks (expects empty array)
- [ ] T071 [P] [US3] Write integration test for user 1 attempting to access user 2's task (expects 403 or 404)
- [ ] T072 [US3] Write integration test for user 1 attempting to update user 2's task (expects 403 or 404)
- [ ] T073 [US3] Write integration test for user 1 attempting to delete user 2's task (expects 403 or 404)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently. User isolation is enforced at the service layer.

---

## Phase 6: User Story 4 - User Authentication and Management (Priority: P4)

**Goal**: Users can register accounts, log in securely, and maintain authenticated sessions, with the system managing user identity through Better Auth.

**Independent Test**: Register a new user account, log in with credentials, receive an authentication token/session, and make authenticated API requests that automatically associate tasks with the logged-in user. Log out and verify the session is invalidated.

### Implementation for User Story 4

- [x] T074 [P] [US4] Research Better Auth Python SDK documentation and integration patterns
- [x] T075 [P] [US4] Install Better Auth dependencies (or alternative auth library if Better Auth unavailable)
- [x] T076 [P] [US4] Create phase-2/src/schemas/user.py with UserRegister, UserLogin, UserResponse schemas
- [x] T077 [US4] Create phase-2/src/services/auth_service.py with register_user and login_user methods
- [x] T078 [US4] Implement password hashing in auth_service.py (using bcrypt or Better Auth)
- [x] T079 [US4] Implement session token generation in auth_service.py (JWT or Better Auth tokens)
- [x] T080 [US4] Create phase-2/src/api/auth.py with APIRouter for authentication endpoints
- [x] T081 [US4] Implement POST /auth/register endpoint in phase-2/src/api/auth.py
- [x] T082 [US4] Implement POST /auth/login endpoint in phase-2/src/api/auth.py
- [x] T083 [US4] Implement POST /auth/logout endpoint in phase-2/src/api/auth.py
- [x] T084 [US4] Add auth router to FastAPI app in phase-2/src/main.py
- [x] T085 [US4] Create get_current_user dependency in phase-2/src/api/deps.py for authentication
- [x] T086 [US4] Add authentication validation to get_current_user (verify token/session)
- [x] T087 [US4] Update POST /tasks to use get_current_user dependency in phase-2/src/api/tasks.py
- [x] T088 [US4] Update GET /tasks to use get_current_user and auto-filter by authenticated user
- [x] T089 [US4] Update GET /tasks/{id} to use get_current_user dependency
- [x] T090 [US4] Update PUT /tasks/{id} to use get_current_user dependency
- [x] T091 [US4] Update PATCH /tasks/{id} to use get_current_user dependency
- [x] T092 [US4] Update DELETE /tasks/{id} to use get_current_user dependency
- [x] T093 [US4] Remove user_id from TaskCreate schema (auto-assigned from authenticated user)
- [x] T094 [US4] Add error handling for 401 Unauthorized when token is missing or invalid
- [x] T095 [US4] Add error handling for duplicate email in POST /auth/register (expects 400 Bad Request)
- [x] T096 [US4] Add error handling for invalid credentials in POST /auth/login (expects 401 Unauthorized)

### Integration Tests for User Story 4 (Optional)

- [ ] T097 [P] [US4] Create phase-2/tests/integration/test_auth_api.py
- [ ] T098 [P] [US4] Write integration test for POST /auth/register with valid data (expects 201 Created)
- [ ] T099 [P] [US4] Write integration test for POST /auth/register with duplicate email (expects 400 Bad Request)
- [ ] T100 [P] [US4] Write integration test for POST /auth/login with valid credentials (expects 200 OK with token)
- [ ] T101 [P] [US4] Write integration test for POST /auth/login with invalid credentials (expects 401 Unauthorized)
- [ ] T102 [US4] Write integration test for POST /auth/logout (expects 204 No Content)
- [ ] T103 [US4] Write integration test for authenticated POST /tasks (task auto-assigned to user)
- [ ] T104 [US4] Write integration test for authenticated GET /tasks (only returns user's tasks)
- [ ] T105 [US4] Write integration test for unauthenticated request to protected endpoint (expects 401)

**Checkpoint**: All user stories should now be independently functional. Full authentication and user isolation are implemented.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T106 [P] Add comprehensive error handling middleware in phase-2/src/main.py
- [x] T107 [P] Add request logging middleware in phase-2/src/main.py
- [x] T108 [P] Create phase-2/tests/unit/test_task_service.py with unit tests for task service
- [x] T109 [P] Create phase-2/tests/unit/test_auth_service.py with unit tests for auth service
- [x] T110 [P] Update phase-2/README.md with complete setup and usage instructions
- [ ] T111 Validate quickstart.md instructions by following them step-by-step
- [ ] T112 Run all integration tests and ensure 100% pass rate
- [x] T113 [P] Add API documentation comments to all endpoints
- [ ] T114 [P] Verify OpenAPI documentation at /docs matches contracts/openapi.yaml
- [x] T115 Add input sanitization for SQL injection prevention (verify SQLModel handles this)
- [x] T116 Add rate limiting consideration documentation (out of scope but document for future)
- [x] T117 Verify all environment variables are documented in .env.example
- [ ] T118 Run manual testing of all acceptance scenarios from spec.md
- [ ] T119 Performance test: Verify API responds within 500ms for 95% of requests
- [x] T120 Security review: Verify passwords are hashed, tokens are secure, user isolation works

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 endpoints but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Enhances US1/US2 with filtering but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Integrates with all previous stories but independently testable

### Within Each User Story

- Implementation tasks before integration tests (tests verify implementation)
- Models before services (services depend on models)
- Services before endpoints (endpoints depend on services)
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T003, T004, T005 can run in parallel
- **Phase 2 (Foundational)**: T009, T010, T011, T012 can run in parallel (module init files)
- **User Story 1**: T021 (schemas) can run in parallel with T033, T034 (test setup)
- **User Story 2**: T041 (schema), T053-T057 (tests) can run in parallel
- **User Story 3**: T069-T072 (tests) can run in parallel
- **User Story 4**: T074, T075, T076 can run in parallel; T097-T101 (tests) can run in parallel
- **Phase 7 (Polish)**: T106, T107, T108, T109, T110, T113, T114, T117 can run in parallel
- **Different user stories can be worked on in parallel by different team members after Foundational phase**

---

## Parallel Example: User Story 1

```bash
# Launch schema creation and test setup together:
Task T021: "Create phase-2/src/schemas/task.py with TaskCreate, TaskUpdate, TaskResponse"
Task T033: "Create phase-2/tests/conftest.py with pytest fixtures"
Task T034: "Create phase-2/tests/integration/test_tasks_api.py"

# Launch all integration tests for User Story 1 together (after implementation):
Task T035: "Write integration test for POST /tasks with valid data"
Task T036: "Write integration test for GET /tasks"
Task T037: "Write integration test for GET /tasks/{id} with existing task"
Task T038: "Write integration test for GET /tasks/{id} with non-existent task"
Task T039: "Write integration test for POST /tasks with missing required fields"
Task T040: "Write integration test for data persistence across server restarts"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T020) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T021-T040)
4. **STOP and VALIDATE**: Test User Story 1 independently using acceptance scenarios
5. Deploy/demo if ready - you now have a working persistent task API!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T020)
2. Add User Story 1 → Test independently → Deploy/Demo (T021-T040) - **MVP!**
3. Add User Story 2 → Test independently → Deploy/Demo (T041-T058) - Full CRUD
4. Add User Story 3 → Test independently → Deploy/Demo (T059-T073) - Multi-user support
5. Add User Story 4 → Test independently → Deploy/Demo (T074-T105) - Production-ready auth
6. Polish → Final validation → Production deployment (T106-T120)

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T020)
2. Once Foundational is done:
   - Developer A: User Story 1 (T021-T040)
   - Developer B: User Story 2 (T041-T058) - can start in parallel
   - Developer C: User Story 3 (T059-T073) - can start in parallel
   - Developer D: User Story 4 (T074-T105) - can start in parallel
3. Stories complete and integrate independently
4. Team collaborates on Polish phase (T106-T120)

---

## Task Summary

- **Total Tasks**: 120
- **Setup Phase**: 5 tasks
- **Foundational Phase**: 15 tasks (BLOCKS all user stories)
- **User Story 1 (P1 - MVP)**: 20 tasks (12 implementation + 8 optional tests)
- **User Story 2 (P2)**: 18 tasks (12 implementation + 6 optional tests)
- **User Story 3 (P3)**: 15 tasks (10 implementation + 5 optional tests)
- **User Story 4 (P4)**: 32 tasks (23 implementation + 9 optional tests)
- **Polish Phase**: 15 tasks

**Parallel Opportunities**: 35+ tasks marked [P] can run in parallel within their phases

**MVP Scope**: Phases 1-3 (T001-T040) = 40 tasks for a working persistent task API

**Independent Test Criteria**:
- US1: Create and retrieve tasks, verify persistence across restarts
- US2: Full CRUD operations on tasks
- US3: User isolation prevents cross-user access
- US4: Authentication required, tasks auto-assigned to authenticated user

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Integration tests are optional but recommended for quality assurance
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Better Auth integration (US4) may require adjustments based on actual SDK documentation
- All paths are relative to `/phase-2/` directory per constitution principle I
