# Feature Specification: Phase 2 - Todo Full-Stack Web Application

**Feature Branch**: `002-web-api-persistence`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Generate the formal specification for Phase 2: Todo Full-Stack Web Application. Evolve the Phase 1 Todo logic into a persistent Web API with FastAPI, Neon Serverless PostgreSQL, SQLModel ORM, Better Auth integration, and user isolation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and Retrieve Tasks via API (Priority: P1) 🎯 MVP

API consumers can create new tasks and retrieve all tasks through REST endpoints, with data persisting across application restarts.

**Why this priority**: This is the foundational capability that transforms Phase 1's in-memory CLI into a persistent web service. Without this, no other features can function. It delivers immediate value by enabling task creation and retrieval via HTTP.

**Independent Test**: Can be fully tested by making POST requests to create tasks and GET requests to retrieve them. Restart the server and verify tasks still exist. Delivers a working API that external clients can integrate with.

**Acceptance Scenarios**:

1. **Given** the API is running, **When** a client sends POST /tasks with valid task data (title, description), **Then** the API returns 201 Created with the task object including generated ID and timestamps
2. **Given** tasks exist in the database, **When** a client sends GET /tasks, **Then** the API returns 200 OK with an array of all tasks
3. **Given** a task was created, **When** the server restarts and a client sends GET /tasks, **Then** the previously created task is still present in the response
4. **Given** a client sends POST /tasks with missing required fields, **When** the request is processed, **Then** the API returns 400 Bad Request with validation error details
5. **Given** a specific task ID exists, **When** a client sends GET /tasks/{id}, **Then** the API returns 200 OK with that specific task object
6. **Given** a task ID does not exist, **When** a client sends GET /tasks/{id}, **Then** the API returns 404 Not Found

---

### User Story 2 - Update and Delete Tasks via API (Priority: P2)

API consumers can modify existing task details and permanently remove tasks they no longer need.

**Why this priority**: Completes the CRUD operations, making the API fully functional for task management. Builds on P1's create/read foundation to enable complete lifecycle management.

**Independent Test**: Create a task via POST, update it via PUT/PATCH, verify changes via GET, delete it via DELETE, and confirm it's gone with another GET. All operations should return appropriate status codes.

**Acceptance Scenarios**:

1. **Given** a task exists with ID 5, **When** a client sends PUT /tasks/5 with updated title and description, **Then** the API returns 200 OK with the updated task object
2. **Given** a task exists with ID 5, **When** a client sends PATCH /tasks/5 with only a status change, **Then** the API returns 200 OK with the task showing the new status
3. **Given** a task exists with ID 5, **When** a client sends DELETE /tasks/5, **Then** the API returns 204 No Content and subsequent GET /tasks/5 returns 404 Not Found
4. **Given** a client sends PUT /tasks/999 where ID 999 does not exist, **When** the request is processed, **Then** the API returns 404 Not Found
5. **Given** a client sends PUT /tasks/5 with invalid data (empty title), **When** the request is processed, **Then** the API returns 400 Bad Request with validation errors

---

### User Story 3 - User Isolation and Task Filtering (Priority: P3)

Each user can only see and manage their own tasks, with the system automatically filtering tasks based on the authenticated user's identity.

**Why this priority**: Enables multi-user support and prepares the foundation for authentication. Without this, all users would see all tasks, making the system unsuitable for production use.

**Independent Test**: Create tasks with different user_id values. Query GET /tasks?user_id=1 and verify only tasks belonging to user 1 are returned. Attempt to update/delete a task belonging to a different user and verify appropriate access control.

**Acceptance Scenarios**:

1. **Given** tasks exist for user_id 1 and user_id 2, **When** a client sends GET /tasks?user_id=1, **Then** the API returns only tasks where user_id equals 1
2. **Given** a client creates a task with POST /tasks including user_id in the payload, **When** the task is created, **Then** the task is associated with that user_id
3. **Given** user 1 is authenticated, **When** they send GET /tasks, **Then** the API automatically filters to show only their tasks (user_id=1)
4. **Given** a task with ID 5 belongs to user_id 2, **When** user 1 attempts PUT /tasks/5, **Then** the API returns 403 Forbidden or 404 Not Found
5. **Given** no tasks exist for user_id 3, **When** a client sends GET /tasks?user_id=3, **Then** the API returns 200 OK with an empty array

---

### User Story 4 - User Authentication and Management (Priority: P4)

Users can register accounts, log in securely, and maintain authenticated sessions, with the system managing user identity through Better Auth.

**Why this priority**: Provides secure user management and authentication, replacing manual user_id passing with proper session-based authentication. This is the final piece for a production-ready multi-user system.

**Independent Test**: Register a new user account, log in with credentials, receive an authentication token/session, and make authenticated API requests that automatically associate tasks with the logged-in user. Log out and verify the session is invalidated.

**Acceptance Scenarios**:

1. **Given** a new user provides email and password, **When** they send POST /auth/register, **Then** the system creates a user account and returns 201 Created with user details (excluding password)
2. **Given** a registered user provides correct credentials, **When** they send POST /auth/login, **Then** the system returns 200 OK with an authentication token/session cookie
3. **Given** a user is authenticated with a valid session, **When** they send POST /tasks without specifying user_id, **Then** the task is automatically associated with their user_id from the session
4. **Given** a user is authenticated, **When** they send GET /tasks, **Then** the API returns only their tasks without requiring a user_id query parameter
5. **Given** a user sends a request without authentication, **When** they attempt to access protected endpoints, **Then** the API returns 401 Unauthorized
6. **Given** a user is logged in, **When** they send POST /auth/logout, **Then** their session is invalidated and subsequent requests return 401 Unauthorized

---

### Edge Cases

- What happens when a client sends a request with an invalid user_id format (non-integer, negative)?
- How does the system handle concurrent updates to the same task by different users?
- What happens when the database connection is lost during a request?
- How does the API handle extremely long task descriptions (e.g., 10,000+ characters)?
- What happens when a user attempts to create a task with a user_id that doesn't exist in the users table?
- How does the system handle malformed JSON in request bodies?
- What happens when Better Auth service is unavailable during authentication attempts?
- How does the API respond to requests with missing or invalid Content-Type headers?
- What happens when a user attempts to register with an email that already exists?
- How does the system handle database schema migrations when the application is running?

## Requirements *(mandatory)*

### Functional Requirements

#### API Endpoints

- **FR-001**: System MUST provide POST /tasks endpoint to create new tasks with title, description, and user_id
- **FR-002**: System MUST provide GET /tasks endpoint to retrieve all tasks with optional user_id filtering
- **FR-003**: System MUST provide GET /tasks/{id} endpoint to retrieve a specific task by ID
- **FR-004**: System MUST provide PUT /tasks/{id} endpoint to update all fields of an existing task
- **FR-005**: System MUST provide PATCH /tasks/{id} endpoint to partially update specific fields of a task
- **FR-006**: System MUST provide DELETE /tasks/{id} endpoint to permanently remove a task
- **FR-007**: System MUST provide POST /auth/register endpoint for user registration
- **FR-008**: System MUST provide POST /auth/login endpoint for user authentication
- **FR-009**: System MUST provide POST /auth/logout endpoint to invalidate user sessions

#### Data Validation

- **FR-010**: System MUST validate that task title is non-empty and does not exceed 200 characters
- **FR-011**: System MUST validate that task description does not exceed 2000 characters
- **FR-012**: System MUST validate that task status is one of: "pending", "in_progress", "complete"
- **FR-013**: System MUST validate that user_id is a positive integer when provided
- **FR-014**: System MUST return 400 Bad Request with detailed validation errors for invalid input

#### Data Persistence

- **FR-015**: System MUST persist all task data to Neon Serverless PostgreSQL database
- **FR-016**: System MUST automatically generate unique task IDs using database auto-increment
- **FR-017**: System MUST automatically set created_at timestamp when a task is created
- **FR-018**: System MUST automatically update updated_at timestamp when a task is modified
- **FR-019**: System MUST maintain data integrity across application restarts

#### User Isolation

- **FR-020**: System MUST filter tasks by user_id when the query parameter is provided
- **FR-021**: System MUST prevent users from accessing tasks belonging to other users
- **FR-022**: System MUST automatically associate tasks with the authenticated user's ID when creating tasks
- **FR-023**: System MUST return 403 Forbidden when a user attempts to modify another user's task

#### Authentication

- **FR-024**: System MUST integrate Better Auth for user registration and authentication
- **FR-025**: System MUST securely hash and store user passwords (handled by Better Auth)
- **FR-026**: System MUST validate user credentials during login
- **FR-027**: System MUST issue session tokens/cookies upon successful authentication
- **FR-028**: System MUST validate session tokens on protected endpoints
- **FR-029**: System MUST return 401 Unauthorized for requests without valid authentication

#### API Response Codes

- **FR-030**: System MUST return 200 OK for successful GET, PUT, PATCH requests
- **FR-031**: System MUST return 201 Created for successful POST requests that create resources
- **FR-032**: System MUST return 204 No Content for successful DELETE requests
- **FR-033**: System MUST return 400 Bad Request for validation errors with error details
- **FR-034**: System MUST return 401 Unauthorized for authentication failures
- **FR-035**: System MUST return 403 Forbidden for authorization failures
- **FR-036**: System MUST return 404 Not Found when requested resources don't exist
- **FR-037**: System MUST return 500 Internal Server Error for unexpected server errors

#### Project Structure

- **FR-038**: System MUST contain all Phase 2 code within the /phase-2 directory
- **FR-039**: System MUST use UV for Python dependency management
- **FR-040**: System MUST maintain separate configuration for development and production environments

### Key Entities

- **Task**: Represents a todo item with the following attributes:
  - id: Unique identifier (auto-generated, positive integer)
  - user_id: Foreign key reference to the user who owns this task (positive integer)
  - title: Short summary of the task (1-200 characters, required)
  - description: Detailed description of the task (0-2000 characters, optional)
  - status: Current state of the task (enum: "pending", "in_progress", "complete", defaults to "pending")
  - created_at: Timestamp when the task was created (auto-generated, ISO 8601 format)
  - updated_at: Timestamp when the task was last modified (auto-updated, ISO 8601 format)

- **User**: Represents a registered user account (managed by Better Auth):
  - id: Unique identifier (auto-generated, positive integer)
  - email: User's email address (unique, required for authentication)
  - password_hash: Securely hashed password (managed by Better Auth)
  - created_at: Timestamp when the account was created
  - Additional fields as defined by Better Auth (name, profile data, etc.)

### Assumptions

- Task status defaults to "pending" when not specified during creation
- Better Auth will handle password hashing, session management, and token generation
- Database connection pooling will be handled by SQLModel/SQLAlchemy
- API will use JSON for all request and response bodies
- Timestamps will be stored in UTC and returned in ISO 8601 format
- User_ID will be required for all task operations (either from session or query parameter)
- Database schema migrations will be handled manually or via Alembic (to be determined in planning)
- API will run on a single server instance (no distributed system considerations for Phase 2)
- CORS will be configured to allow requests from any origin (for development; to be restricted in production)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: API endpoints respond to valid requests within 500ms for 95% of requests under normal load
- **SC-002**: System successfully persists 100% of valid task creation requests to the database
- **SC-003**: Tasks remain accessible after server restarts, with 100% data retention
- **SC-004**: User isolation prevents 100% of unauthorized access attempts to other users' tasks
- **SC-005**: API returns correct HTTP status codes for all request scenarios (success, validation errors, not found, unauthorized)
- **SC-006**: System handles 100 concurrent API requests without errors or data corruption
- **SC-007**: User registration and login complete successfully within 2 seconds for 95% of attempts
- **SC-008**: Database schema correctly enforces all constraints (non-null, foreign keys, unique constraints)
- **SC-009**: API validation catches 100% of invalid input and returns descriptive error messages
- **SC-010**: Authenticated users can perform all CRUD operations on their own tasks with 100% success rate

### Quality Criteria

- All API endpoints documented with request/response examples
- Database schema validated against requirements
- Integration tests cover all user stories
- Error responses include actionable error messages
- API follows RESTful conventions for resource naming and HTTP methods

## Constraints

- All work must be contained within the /phase-2 directory
- Must use Python 3.13+ as the runtime environment
- Must use FastAPI as the web framework
- Must use Neon Serverless PostgreSQL as the database
- Must use SQLModel as the ORM
- Must use Better Auth for authentication
- Must use UV for dependency management
- No frontend UI development in this phase
- No AI agents or LLM integration in this phase
- No file upload or media handling in this phase

## Out of Scope

- Frontend user interface (web or mobile)
- Real-time updates via WebSockets
- Task sharing or collaboration features
- Task categories, tags, or labels
- Task due dates or reminders
- Task priority levels
- Bulk operations (bulk delete, bulk update)
- Task search or filtering beyond user_id
- Task sorting or pagination
- Rate limiting or API throttling
- Advanced authentication (OAuth, SSO, MFA)
- Role-based access control (RBAC) beyond basic user isolation
- Task history or audit logs
- Soft deletes (deleted tasks are permanently removed)
- Task attachments or file uploads
- Email notifications
- API versioning
- GraphQL API (REST only)

## Dependencies

- Neon Serverless PostgreSQL account and database instance
- Better Auth service/library availability
- UV package manager installed
- Python 3.13+ runtime environment
- Network connectivity to Neon database
- Environment variables for database connection strings and auth secrets

## Risks

- **Database Connection Failures**: Neon Serverless PostgreSQL may have cold start latency or connection limits
  - Mitigation: Implement connection pooling and retry logic

- **Better Auth Integration Complexity**: Better Auth may have specific integration requirements or limitations
  - Mitigation: Review Better Auth documentation early in planning phase

- **User Isolation Bugs**: Incorrect filtering logic could expose tasks to wrong users
  - Mitigation: Comprehensive integration tests for user isolation scenarios

- **Database Schema Changes**: Schema evolution may require migration strategy
  - Mitigation: Plan for database migration tooling (Alembic) in design phase

## Next Steps

1. Run `/sp.clarify` if any requirements need clarification
2. Run `/sp.plan` to create the technical implementation plan
3. Run `/sp.tasks` to generate the task breakdown for implementation
