# Implementation Plan: AI Agent & MCP Integration

**Branch**: `003-ai-agent-mcp` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-agent-mcp/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Phase 3 adds a modern Next.js 15+ web frontend with AI-powered task management capabilities. Users can manage tasks through a visual dashboard or via natural language chat powered by OpenAI Agents SDK. The implementation includes Better Auth integration with the existing Neon PostgreSQL database from Phase 2, a separate MCP server exposing Phase 2 CRUD operations as executable tools, and a chat interface enabling conversational task management. The architecture maintains strict phase isolation while enabling secure communication between frontend, AI agent, and backend services.

## Technical Context

**Language/Version**: TypeScript 5.3+, Node.js 18+, Python 3.13+ (Phase 2 backend)
**Primary Dependencies**: Next.js 15+ (App Router), Better Auth, OpenAI Agents SDK, MCP SDK, Shadcn UI, Tailwind CSS, Lucide Icons
**Storage**: Neon Serverless PostgreSQL (shared with Phase 2), SessionStorage (chat history - MVP scope)
**Testing**: Vitest (unit), Playwright (e2e), pytest (Phase 2 backend)
**Target Platform**: Web (modern browsers), Node.js server runtime
**Project Type**: Web application (frontend + MCP server + existing backend)
**Performance Goals**:
- Dashboard task list load: <2s for 100 tasks
- AI chat response: <2s for 95% of requests
- Task creation via chat: <15s end-to-end
- Task creation via dashboard: <30s end-to-end
**Constraints**:
- Phase isolation: All Phase 3 code in /phase-3 directory
- No modifications to Phase 2 backend code
- JWT token authentication for API communication
- OpenAI API rate limits and costs
- MCP server must be stateless
**Scale/Scope**:
- MVP: Single user concurrent sessions
- 100-1000 tasks per user
- 5 MCP tools (add_task, list_tasks, update_task, delete_task, get_task)
- 3 main UI screens (Dashboard, Login, Chat)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Phase Isolation
- **Status**: PASS
- **Evidence**: All Phase 3 code contained in `/phase-3` directory. Phase 2 backend remains untouched in `/phase-2`. Communication via HTTP APIs only.
- **Verification**: Directory structure enforces isolation. No cross-phase imports possible.

### ✅ Spec-Driven Development
- **Status**: PASS
- **Evidence**: Complete specification exists at `specs/003-ai-agent-mcp/spec.md` with 4 prioritized user stories, 47 functional requirements, 12 measurable success criteria.
- **Verification**: Specification approved and validated via requirements checklist. All quality gates passed.

### ✅ Scope Discipline
- **Status**: PASS
- **Evidence**: Clear boundaries defined. Out of scope: advanced AI features, real-time collaboration, mobile apps, analytics, notifications, multi-language support, offline mode, task templates, bulk operations, export/import, advanced search, task dependencies, recurring tasks, file attachments, task comments, activity logs.
- **Verification**: 15 explicit out-of-scope items documented in spec.md.

### ✅ Protected Directories
- **Status**: PASS
- **Evidence**: No modifications to `/phase-1` or `/phase-2` directories. All work in `/phase-3`.
- **Verification**: Git status shows no changes to protected directories.

### ✅ Verification-First
- **Status**: PASS
- **Evidence**: Plan references existing Phase 2 API endpoints (`/api/auth/*`, `/api/tasks/*`). Better Auth configuration verified against Neon database schema from Phase 2.
- **Verification**: Phase 2 backend running and accessible. Database schema documented in `phase-2/docs/`.

### ✅ Evolutionary Architecture
- **Status**: PASS
- **Evidence**: Architecture supports incremental delivery. P1 (Dashboard) can be deployed independently. P2 (Auth) builds on P1. P3 (Chat) and P4 (AI) are additive enhancements.
- **Verification**: User stories are independently testable and deliverable.

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-agent-mcp/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── mcp-tools.json   # MCP tool definitions
│   └── frontend-api.md  # Frontend-backend API contracts
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase-3/
├── frontend/                    # Next.js 15+ application
│   ├── app/                     # App Router pages
│   │   ├── (auth)/              # Auth route group
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   ├── (dashboard)/         # Protected route group
│   │   │   ├── layout.tsx       # Dashboard layout with chat sidebar
│   │   │   └── page.tsx         # Main dashboard
│   │   ├── api/                 # API routes
│   │   │   ├── auth/            # Better Auth endpoints
│   │   │   │   └── [...all]/route.ts
│   │   │   └── chat/            # AI chat endpoints
│   │   │       └── route.ts
│   │   ├── layout.tsx           # Root layout
│   │   └── page.tsx             # Landing/redirect page
│   ├── components/              # React components
│   │   ├── ui/                  # Shadcn UI components
│   │   ├── dashboard/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── TaskFilters.tsx
│   │   ├── chat/
│   │   │   ├── ChatSidebar.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── ChatHistory.tsx
│   │   └── auth/
│   │       ├── LoginForm.tsx
│   │       └── SignupForm.tsx
│   ├── lib/                     # Utilities and configurations
│   │   ├── auth.ts              # Better Auth configuration
│   │   ├── api-client.ts        # Phase 2 API client
│   │   ├── ai-agent.ts          # OpenAI Agents SDK setup
│   │   └── utils.ts             # Helper functions
│   ├── hooks/                   # Custom React hooks
│   │   ├── useAuth.ts
│   │   ├── useTasks.ts
│   │   └── useChat.ts
│   ├── types/                   # TypeScript type definitions
│   │   ├── task.ts
│   │   ├── user.ts
│   │   └── chat.ts
│   ├── public/                  # Static assets
│   ├── .env.local.example       # Environment variables template
│   ├── next.config.js           # Next.js configuration
│   ├── tailwind.config.ts       # Tailwind CSS configuration
│   ├── tsconfig.json            # TypeScript configuration
│   ├── package.json             # Dependencies
│   └── README.md                # Frontend setup instructions
│
├── mcp-server/                  # MCP server (separate service)
│   ├── src/
│   │   ├── index.ts             # MCP server entry point
│   │   ├── tools/               # MCP tool implementations
│   │   │   ├── add-task.ts
│   │   │   ├── list-tasks.ts
│   │   │   ├── update-task.ts
│   │   │   ├── delete-task.ts
│   │   │   └── get-task.ts
│   │   ├── client.ts            # Phase 2 API client
│   │   └── types.ts             # Type definitions
│   ├── .env.example             # Environment variables template
│   ├── tsconfig.json            # TypeScript configuration
│   ├── package.json             # Dependencies
│   └── README.md                # MCP server setup instructions
│
├── tests/                       # Test suites
│   ├── e2e/                     # End-to-end tests (Playwright)
│   │   ├── auth.spec.ts
│   │   ├── dashboard.spec.ts
│   │   └── chat.spec.ts
│   ├── integration/             # Integration tests
│   │   ├── mcp-tools.test.ts
│   │   └── api-client.test.ts
│   └── unit/                    # Unit tests (Vitest)
│       ├── components/
│       ├── hooks/
│       └── lib/
│
├── .env.example                 # Root environment variables
├── .gitignore                   # Git ignore rules
├── package.json                 # Root package.json (workspace)
└── README.md                    # Phase 3 overview and setup
```

**Structure Decision**: Web application structure with separate frontend and MCP server. The frontend uses Next.js 15+ App Router with route groups for authentication and protected dashboard routes. The MCP server is a standalone TypeScript service that exposes Phase 2 CRUD operations as MCP tools. This separation ensures security (MCP server can run in isolated environment), maintainability (clear service boundaries), and scalability (services can be deployed independently).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All constitution gates passed.

## Architecture Decisions

### AD-001: MCP Server as Separate Service

**Context**: Need to expose Phase 2 CRUD operations as MCP tools for AI agent consumption.

**Options Considered**:
1. **Separate MCP server** (TypeScript service)
2. Embed MCP tools in Next.js API routes
3. Direct AI agent to Phase 2 API calls

**Decision**: Separate MCP server (Option 1)

**Rationale**:
- **Security**: MCP server can run in isolated environment with restricted network access to Phase 2 backend
- **Separation of Concerns**: Clear boundary between AI agent orchestration (Next.js) and tool execution (MCP server)
- **Reusability**: MCP tools can be consumed by other AI agents or services in future
- **Testability**: MCP server can be tested independently without Next.js runtime
- **Phase Isolation**: MCP server acts as adapter layer, preventing direct coupling between Phase 3 frontend and Phase 2 backend

**Trade-offs**:
- Additional service to deploy and monitor
- Network latency between Next.js API routes and MCP server
- More complex local development setup

**Mitigation**:
- Use Docker Compose for local development to simplify multi-service setup
- Implement health checks and monitoring for MCP server
- Document deployment requirements clearly in quickstart.md

### AD-002: Better Auth with Neon PostgreSQL

**Context**: Need authentication system that integrates with existing Phase 2 database.

**Options Considered**:
1. **Better Auth with Neon PostgreSQL** (shared database)
2. NextAuth.js with separate authentication database
3. Clerk or Auth0 (third-party service)

**Decision**: Better Auth with Neon PostgreSQL (Option 1)

**Rationale**:
- **Single Source of Truth**: User records in same database as tasks, ensuring data consistency
- **Simplified Architecture**: No need to sync users across multiple databases
- **Cost Efficiency**: Reuse existing Neon database, no additional database costs
- **Better Auth Advantages**: Modern, TypeScript-first, flexible, supports multiple auth methods
- **Phase 2 Compatibility**: Better Auth can use existing `users` table from Phase 2

**Trade-offs**:
- Tight coupling between Phase 2 and Phase 3 at database level
- Database schema changes require coordination across phases
- Better Auth is newer, less mature than NextAuth.js

**Mitigation**:
- Document database schema dependencies clearly
- Use Alembic migrations (Phase 2 tool) for any schema changes
- Better Auth's flexibility allows adaptation if requirements change

### AD-003: Session Storage for Chat History (MVP Scope)

**Context**: Need to persist chat messages for user experience.

**Options Considered**:
1. **SessionStorage** (browser-only, MVP scope)
2. Database persistence (Neon PostgreSQL)
3. Redis or in-memory cache

**Decision**: SessionStorage (Option 1) for MVP

**Rationale**:
- **Simplicity**: No backend changes required, purely frontend implementation
- **Fast Iteration**: Can ship MVP faster without database schema design
- **Sufficient for MVP**: Chat history within single session meets P3 user story requirements
- **Evolutionary Path**: Can migrate to database persistence in future without breaking changes

**Trade-offs**:
- Chat history lost on page refresh or browser close
- No cross-device chat history
- Limited storage capacity (typically 5-10MB)

**Mitigation**:
- Document limitation clearly in user documentation
- Design chat message schema to be database-ready for future migration
- Implement export/download chat history feature if needed

### AD-004: OpenAI Agents SDK in Next.js API Routes

**Context**: Need to run AI agent that can execute MCP tools.

**Options Considered**:
1. **Server-side in Next.js API routes** (Node.js runtime)
2. Client-side in browser (JavaScript)
3. Separate Python service (FastAPI)

**Decision**: Server-side in Next.js API routes (Option 1)

**Rationale**:
- **Security**: OpenAI API keys never exposed to browser
- **Performance**: Server-side execution faster, no CORS issues
- **Integration**: Direct access to MCP server from same backend
- **Simplicity**: Single deployment unit (Next.js app), no additional service
- **OpenAI Agents SDK Support**: SDK designed for Node.js server environments

**Trade-offs**:
- Next.js API routes have execution time limits (10s on Vercel free tier)
- Node.js runtime required (not edge runtime compatible)
- Increased Next.js server load

**Mitigation**:
- Use streaming responses for long-running AI operations
- Implement timeout handling and graceful degradation
- Document runtime requirements for deployment platforms
- Consider moving to separate service if performance becomes issue

## Phase 0: Research & Technology Validation

**Objective**: Validate technology choices and document best practices.

**Deliverable**: `research.md` with findings on:
1. Next.js 15+ App Router patterns (route groups, server actions, API routes)
2. Better Auth setup with Neon PostgreSQL (configuration, session management, JWT)
3. OpenAI Agents SDK integration (agent creation, tool calling, streaming)
4. MCP SDK usage (server setup, tool definition, error handling)
5. Shadcn UI component library (installation, theming, customization)
6. Phase 2 API authentication (JWT token flow, error handling)

**Success Criteria**:
- All technology choices validated with working proof-of-concept code
- Best practices documented for each technology
- Known limitations and workarounds identified
- Security considerations documented

## Phase 1: Design & Contracts

**Objective**: Define data models and API contracts.

**Deliverables**:
1. `data-model.md`: Entity definitions for User, Task, Chat Message, MCP Tool, AI Agent Session
2. `contracts/mcp-tools.json`: MCP tool schemas (input/output for all 5 tools)
3. `contracts/frontend-api.md`: Frontend-backend API contracts (auth endpoints, chat endpoints)
4. `quickstart.md`: Setup instructions for local development

**Success Criteria**:
- All entities have clear TypeScript type definitions
- MCP tool schemas are valid and testable
- API contracts specify request/response formats, error codes, authentication requirements
- Quickstart guide enables new developer to run Phase 3 locally in <30 minutes

## Phase 2: Implementation Tasks

**Objective**: Generate actionable task list with dependencies.

**Deliverable**: `tasks.md` (generated by `/sp.tasks` command)

**Expected Task Categories**:
1. **Setup & Configuration**: Initialize Next.js project, install dependencies, configure Tailwind/Shadcn
2. **Authentication**: Implement Better Auth, create login/signup pages, JWT token management
3. **Dashboard UI**: Build task list, task cards, task form, filters
4. **MCP Server**: Implement 5 MCP tools, Phase 2 API client, error handling
5. **AI Agent**: Setup OpenAI Agents SDK, implement chat API route, tool calling logic
6. **Chat Interface**: Build chat sidebar, message components, input handling
7. **Integration**: Connect frontend to MCP server, implement end-to-end flows
8. **Testing**: Write unit tests, integration tests, e2e tests
9. **Documentation**: Update README files, write deployment guide

**Success Criteria**:
- Tasks are ordered by dependencies (can be executed sequentially)
- Each task is independently testable
- Each task references specific files and acceptance criteria
- Total task count: 30-50 tasks

## Risks & Mitigation

### High Priority Risks

**R-001: OpenAI API Rate Limits**
- **Impact**: Chat functionality degraded or unavailable during high usage
- **Probability**: Medium
- **Mitigation**: Implement rate limiting on frontend, queue requests, show user-friendly error messages, document API usage limits

**R-002: MCP Server Reliability**
- **Impact**: AI agent cannot execute tools, chat functionality broken
- **Probability**: Medium
- **Mitigation**: Implement health checks, retry logic, fallback to direct API calls, comprehensive error handling

**R-003: Better Auth Configuration Complexity**
- **Impact**: Authentication broken, users cannot login, development blocked
- **Probability**: Medium
- **Mitigation**: Follow Better Auth documentation closely, test with Phase 2 database early, implement comprehensive auth tests

### Medium Priority Risks

**R-004: Phase 2 API Changes**
- **Impact**: Frontend breaks if Phase 2 API changes without notice
- **Probability**: Low
- **Mitigation**: Document API contract, implement API versioning, add integration tests

**R-005: Chat History Loss (SessionStorage)**
- **Impact**: Poor user experience, users lose chat context
- **Probability**: High (by design for MVP)
- **Mitigation**: Document limitation, implement export feature, plan database migration for post-MVP

**R-006: Next.js API Route Timeouts**
- **Impact**: Long-running AI operations fail, poor user experience
- **Probability**: Medium
- **Mitigation**: Implement streaming responses, show progress indicators, set realistic timeout limits

### Low Priority Risks

**R-007: Shadcn UI Component Compatibility**
- **Impact**: UI components don't work as expected, styling issues
- **Probability**: Low
- **Mitigation**: Use stable Shadcn components, test thoroughly, have fallback to custom components

**R-008: TypeScript Type Mismatches**
- **Impact**: Runtime errors, type safety compromised
- **Probability**: Low
- **Mitigation**: Strict TypeScript configuration, comprehensive type definitions, runtime validation with Zod

## Dependencies

### External Services
- **Neon PostgreSQL**: Phase 2 database (existing)
- **OpenAI API**: AI agent functionality (requires API key)
- **Phase 2 FastAPI Backend**: Task CRUD operations (must be running)

### Internal Dependencies
- **Phase 2 Backend**: Must be deployed and accessible
- **Phase 2 Database Schema**: Users and tasks tables must exist
- **Phase 2 API Documentation**: Endpoint specifications required

### Development Tools
- **Node.js 18+**: Runtime for Next.js and MCP server
- **npm/yarn/pnpm**: Package manager
- **Docker** (optional): For local multi-service development
- **Git**: Version control

### Third-Party Libraries
- **Next.js 15+**: Web framework
- **Better Auth**: Authentication
- **OpenAI Agents SDK**: AI agent
- **MCP SDK**: Tool protocol
- **Shadcn UI**: Component library
- **Tailwind CSS**: Styling
- **Lucide Icons**: Icons
- **Vitest**: Unit testing
- **Playwright**: E2E testing

## Open Questions

1. **OpenAI Model Selection**: Which OpenAI model for AI agent? (gpt-4o, gpt-4o-mini, gpt-3.5-turbo)
   - **Impact**: Cost, performance, response quality
   - **Resolution**: Test with gpt-4o-mini for MVP (cost-effective), upgrade if needed

2. **Better Auth OAuth Providers**: Which OAuth providers to support? (Google, GitHub, Email/Password)
   - **Impact**: User onboarding experience, implementation complexity
   - **Resolution**: Start with Email/Password for MVP, add OAuth post-MVP

3. **Deployment Platform**: Where to deploy? (Vercel, Railway, self-hosted)
   - **Impact**: Cost, performance, deployment complexity
   - **Resolution**: Document deployment options in quickstart.md, recommend Vercel for simplicity

4. **Chat Message Persistence**: When to migrate from SessionStorage to database?
   - **Impact**: User experience, development effort
   - **Resolution**: Post-MVP based on user feedback

5. **Task Due Dates**: Should tasks support due dates and reminders?
   - **Impact**: Feature scope, AI agent complexity
   - **Resolution**: Out of scope for MVP (documented in spec.md)

6. **MCP Server Hosting**: Should MCP server be deployed separately or with Next.js?
   - **Impact**: Deployment complexity, security, scalability
   - **Resolution**: Deploy separately for production (security), together for local dev (simplicity)

## Next Steps

1. **Generate research.md**: Run Phase 0 research to validate technology choices
2. **Generate data-model.md**: Define entity schemas and relationships
3. **Generate contracts/**: Create MCP tool schemas and API contracts
4. **Generate quickstart.md**: Write setup instructions for local development
5. **Run `/sp.tasks`**: Generate actionable task list with dependencies
6. **Begin Implementation**: Execute tasks in dependency order

## Success Metrics

**Planning Phase Success**:
- ✅ All architecture decisions documented with rationale
- ✅ All risks identified with mitigation strategies
- ✅ Project structure defined and validated
- ✅ Constitution gates passed
- ⏳ Research artifacts generated (next step)
- ⏳ Design artifacts generated (next step)
- ⏳ Task list generated (next step)

**Implementation Phase Success** (measured after `/sp.tasks` execution):
- All tasks have clear acceptance criteria
- Tasks are ordered by dependencies
- Each task references specific files
- Test coverage plan defined
- Deployment strategy documented
