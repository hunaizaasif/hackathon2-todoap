---
description: "Task list for Phase 3: AI Agent & MCP Integration"
---

# Tasks: AI Agent & MCP Integration

**Input**: Design documents from `/specs/003-ai-agent-mcp/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL for this feature. Include them if time permits, but they are not blocking for MVP delivery.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `phase-3/frontend/`
- **MCP Server**: `phase-3/mcp-server/`
- **Tests**: `phase-3/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create phase-3 directory structure per plan.md
- [x] T002 Initialize Next.js 15+ project in phase-3/frontend with TypeScript and App Router
- [x] T003 [P] Initialize MCP server project in phase-3/mcp-server with TypeScript
- [x] T004 [P] Configure Tailwind CSS in phase-3/frontend/tailwind.config.ts
- [x] T005 [P] Initialize Shadcn UI in phase-3/frontend (run shadcn-ui init)
- [x] T006 [P] Install Shadcn UI components: button, card, input, textarea, dialog, dropdown-menu, badge, separator, scroll-area
- [x] T007 [P] Configure TypeScript strict mode in phase-3/frontend/tsconfig.json
- [x] T008 [P] Configure TypeScript strict mode in phase-3/mcp-server/tsconfig.json
- [x] T009 [P] Create .env.example files in phase-3/frontend/ and phase-3/mcp-server/
- [x] T010 [P] Create .gitignore for phase-3 directory
- [x] T011 [P] Create phase-3/README.md with setup instructions
- [x] T012 [P] Setup ESLint and Prettier for phase-3/frontend
- [x] T013 [P] Setup ESLint and Prettier for phase-3/mcp-server

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T014 Create Alembic migration for Better Auth tables (sessions, verification_tokens) in phase-2/alembic/versions/
- [ ] T015 Run Alembic migration to add Better Auth tables to Phase 2 database
- [x] T016 Create TypeScript type definitions in phase-3/frontend/types/user.ts
- [x] T017 [P] Create TypeScript type definitions in phase-3/frontend/types/task.ts
- [x] T018 [P] Create TypeScript type definitions in phase-3/frontend/types/chat.ts
- [x] T019 [P] Create TypeScript type definitions in phase-3/frontend/types/session.ts
- [x] T020 [P] Create TypeScript type definitions in phase-3/mcp-server/src/types.ts
- [x] T021 Create Phase 2 API client in phase-3/frontend/lib/api-client.ts with JWT token support
- [x] T022 [P] Create utility functions in phase-3/frontend/lib/utils.ts
- [x] T023 Configure Next.js in phase-3/frontend/next.config.js (API routes, runtime config)
- [x] T024 Create root layout in phase-3/frontend/app/layout.tsx with metadata and providers
- [x] T025 Create landing page in phase-3/frontend/app/page.tsx with redirect logic

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View and Manage Tasks via Web Dashboard (Priority: P1) 🎯 MVP

**Goal**: Users can view, create, edit, and delete tasks through a visual dashboard interface

**Independent Test**: Log in, create a task through the UI, view it in the task list, edit it, mark as complete, and delete it. Verify all operations work without requiring AI chat functionality.

### Implementation for User Story 1

- [ ] T026 [P] [US1] Create TaskList component in phase-3/frontend/components/dashboard/TaskList.tsx
- [ ] T027 [P] [US1] Create TaskCard component in phase-3/frontend/components/dashboard/TaskCard.tsx
- [ ] T028 [P] [US1] Create TaskForm component in phase-3/frontend/components/dashboard/TaskForm.tsx
- [ ] T029 [P] [US1] Create TaskFilters component in phase-3/frontend/components/dashboard/TaskFilters.tsx
- [ ] T030 [US1] Create useTasks hook in phase-3/frontend/hooks/useTasks.ts with CRUD operations
- [ ] T031 [US1] Create dashboard route group layout in phase-3/frontend/app/(dashboard)/layout.tsx
- [ ] T032 [US1] Create dashboard page in phase-3/frontend/app/(dashboard)/page.tsx
- [ ] T033 [US1] Implement task creation dialog with form validation
- [ ] T034 [US1] Implement task editing with optimistic updates
- [ ] T035 [US1] Implement task deletion with confirmation dialog
- [ ] T036 [US1] Implement task status toggle (pending/in_progress/complete)
- [ ] T037 [US1] Implement task filtering by status
- [ ] T038 [US1] Add loading states and error handling to dashboard
- [ ] T039 [US1] Add empty state UI when no tasks exist
- [ ] T040 [US1] Implement responsive design for mobile/tablet/desktop

**Checkpoint**: At this point, User Story 1 should be fully functional - users can manage tasks via dashboard (requires temporary auth bypass or manual token for testing)

---

## Phase 4: User Story 2 - Secure Authentication with Better Auth (Priority: P2)

**Goal**: Users can securely register, log in, log out, and maintain authenticated sessions

**Independent Test**: Register a new account, log in, verify session persists across page refreshes, log out, attempt to access dashboard while unauthenticated (should redirect to login). Verify user isolation by creating tasks with different accounts.

### Implementation for User Story 2

- [ ] T041 [US2] Configure Better Auth in phase-3/frontend/lib/auth.ts with Neon PostgreSQL adapter
- [ ] T042 [US2] Create Better Auth API route handler in phase-3/frontend/app/api/auth/[...all]/route.ts
- [ ] T043 [P] [US2] Create LoginForm component in phase-3/frontend/components/auth/LoginForm.tsx
- [ ] T044 [P] [US2] Create SignupForm component in phase-3/frontend/components/auth/SignupForm.tsx
- [ ] T045 [US2] Create auth route group layout in phase-3/frontend/app/(auth)/layout.tsx
- [ ] T046 [P] [US2] Create login page in phase-3/frontend/app/(auth)/login/page.tsx
- [ ] T047 [P] [US2] Create signup page in phase-3/frontend/app/(auth)/signup/page.tsx
- [ ] T048 [US2] Create useAuth hook in phase-3/frontend/hooks/useAuth.ts
- [ ] T049 [US2] Create authentication middleware in phase-3/frontend/middleware.ts
- [ ] T050 [US2] Implement session validation and token refresh logic
- [ ] T051 [US2] Add logout functionality to dashboard layout
- [ ] T052 [US2] Implement protected route redirects for unauthenticated users
- [ ] T053 [US2] Add form validation for email and password (min 8 chars, complexity)
- [ ] T054 [US2] Implement error handling for auth failures (invalid credentials, duplicate email)
- [ ] T055 [US2] Update dashboard to use authenticated user context
- [ ] T056 [US2] Update API client to include JWT token from Better Auth session

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - users can register, log in, and manage their own tasks securely

---

## Phase 5: User Story 3 - Manage Tasks via Natural Language Chat (Priority: P3)

**Goal**: Users can create, view, update, and delete tasks using conversational natural language commands

**Independent Test**: Open chat sidebar, type "Create a task to buy milk", verify task is created. Type "Show my tasks", verify tasks are listed. Type "Mark buy milk as complete", verify task status updates. Type "Delete the milk task", verify task is deleted. All operations should work through natural language without using the dashboard UI.

### MCP Server Implementation

- [ ] T057 [P] [US3] Create MCP server entry point in phase-3/mcp-server/src/index.ts
- [ ] T058 [P] [US3] Create Phase 2 API client in phase-3/mcp-server/src/client.ts with JWT support
- [ ] T059 [P] [US3] Implement add_task MCP tool in phase-3/mcp-server/src/tools/add-task.ts
- [ ] T060 [P] [US3] Implement list_tasks MCP tool in phase-3/mcp-server/src/tools/list-tasks.ts
- [ ] T061 [P] [US3] Implement get_task MCP tool in phase-3/mcp-server/src/tools/get-task.ts
- [ ] T062 [P] [US3] Implement update_task MCP tool in phase-3/mcp-server/src/tools/update-task.ts
- [ ] T063 [P] [US3] Implement delete_task MCP tool in phase-3/mcp-server/src/tools/delete-task.ts
- [ ] T064 [US3] Register all MCP tools with tool discovery endpoint
- [ ] T065 [US3] Implement MCP tool execution handler with error handling
- [ ] T066 [US3] Add authentication validation for MCP tool calls
- [ ] T067 [US3] Add logging for all MCP tool executions
- [ ] T068 [US3] Create MCP server README.md with setup instructions

### AI Agent Implementation

- [ ] T069 [US3] Configure OpenAI Agents SDK in phase-3/frontend/lib/ai-agent.ts
- [ ] T070 [US3] Create chat API route in phase-3/frontend/app/api/chat/route.ts
- [ ] T071 [US3] Implement MCP tool discovery from chat API route
- [ ] T072 [US3] Implement tool calling logic with OpenAI function calling
- [ ] T073 [US3] Implement conversation context management (last 10 messages)
- [ ] T074 [US3] Add system prompt for task management AI agent
- [ ] T075 [US3] Implement error handling for OpenAI API failures
- [ ] T076 [US3] Implement rate limiting for chat endpoint (20 req/min per user)
- [ ] T077 [US3] Add timeout handling for long-running AI operations

### Chat Interface Implementation

- [ ] T078 [P] [US3] Create ChatSidebar component in phase-3/frontend/components/chat/ChatSidebar.tsx
- [ ] T079 [P] [US3] Create ChatMessage component in phase-3/frontend/components/chat/ChatMessage.tsx
- [ ] T080 [P] [US3] Create ChatInput component in phase-3/frontend/components/chat/ChatInput.tsx
- [ ] T081 [P] [US3] Create ChatHistory component in phase-3/frontend/components/chat/ChatHistory.tsx
- [ ] T082 [US3] Create useChat hook in phase-3/frontend/hooks/useChat.ts
- [ ] T083 [US3] Implement SessionStorage persistence for chat messages
- [ ] T084 [US3] Add chat sidebar to dashboard layout
- [ ] T085 [US3] Implement chat message rendering with markdown support
- [ ] T086 [US3] Add typing indicator and loading states
- [ ] T087 [US3] Implement auto-scroll to latest message
- [ ] T088 [US3] Add error handling and retry logic for failed messages
- [ ] T089 [US3] Implement chat sidebar toggle (open/close)
- [ ] T090 [US3] Add visual feedback for tool executions in chat
- [ ] T091 [US3] Sync dashboard task list when tasks are created/updated via chat

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work - users can manage tasks via dashboard OR natural language chat

---

## Phase 6: User Story 4 - AI Agent Provides Intelligent Assistance (Priority: P4)

**Goal**: AI agent provides proactive suggestions, task prioritization, and contextual help

**Independent Test**: Ask AI "What should I focus on?", verify it suggests tasks based on data. Ask "How many tasks do I have?", verify it provides accurate summary. Ask "Help me plan my day", verify it provides prioritized suggestions.

### Implementation for User Story 4

- [ ] T092 [US4] Enhance system prompt with intelligent assistance instructions
- [ ] T093 [US4] Implement task analysis logic for prioritization suggestions
- [ ] T094 [US4] Add proactive notifications for overdue tasks (if due dates added)
- [ ] T095 [US4] Implement task summary and statistics generation
- [ ] T096 [US4] Add contextual help responses for vague queries
- [ ] T097 [US4] Implement "plan my day" feature with task prioritization
- [ ] T098 [US4] Add clarifying question logic for ambiguous commands
- [ ] T099 [US4] Enhance chat UI to display AI suggestions prominently
- [ ] T100 [US4] Add feedback mechanism for AI responses (optional)

**Checkpoint**: All user stories should now be independently functional with enhanced AI intelligence

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T101 [P] Update phase-3/frontend/README.md with complete setup instructions
- [ ] T102 [P] Update phase-3/mcp-server/README.md with deployment guide
- [ ] T103 [P] Create phase-3/.env.example with all required environment variables
- [ ] T104 [P] Add comprehensive error boundaries to frontend app
- [ ] T105 [P] Implement global loading state management
- [ ] T106 [P] Add toast notifications for success/error messages
- [ ] T107 [P] Optimize bundle size and implement code splitting
- [ ] T108 [P] Add performance monitoring for API calls
- [ ] T109 [P] Implement proper CORS configuration for production
- [ ] T110 [P] Add security headers to Next.js config
- [ ] T111 [P] Implement proper logging for production debugging
- [ ] T112 [P] Add health check endpoints for frontend and MCP server
- [ ] T113 Validate quickstart.md by following setup instructions
- [ ] T114 Create deployment documentation for Vercel/production
- [ ] T115 [P] Add accessibility improvements (ARIA labels, keyboard navigation)
- [ ] T116 [P] Implement dark mode support (optional)
- [ ] T117 Final integration testing across all user stories
- [ ] T118 Performance testing and optimization

### Optional: Testing Tasks (if time permits)

- [ ] T119 [P] Setup Vitest for unit testing in phase-3/frontend
- [ ] T120 [P] Setup Playwright for e2e testing in phase-3/tests/e2e
- [ ] T121 [P] Write unit tests for useTasks hook in phase-3/tests/unit/hooks/useTasks.test.ts
- [ ] T122 [P] Write unit tests for useAuth hook in phase-3/tests/unit/hooks/useAuth.test.ts
- [ ] T123 [P] Write unit tests for useChat hook in phase-3/tests/unit/hooks/useChat.test.ts
- [ ] T124 [P] Write unit tests for API client in phase-3/tests/unit/lib/api-client.test.ts
- [ ] T125 [P] Write integration tests for MCP tools in phase-3/tests/integration/mcp-tools.test.ts
- [ ] T126 [P] Write e2e test for authentication flow in phase-3/tests/e2e/auth.spec.ts
- [ ] T127 [P] Write e2e test for dashboard task management in phase-3/tests/e2e/dashboard.spec.ts
- [ ] T128 [P] Write e2e test for chat interface in phase-3/tests/e2e/chat.spec.ts

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Requires US1 and US2 for full functionality but core chat can be tested independently
- **User Story 4 (P4)**: Depends on US3 completion - Enhances existing chat functionality

### Within Each User Story

- MCP Server tools can be built in parallel (T059-T063)
- Chat UI components can be built in parallel (T078-T081)
- Auth components can be built in parallel (T043-T044, T046-T047)
- Dashboard components can be built in parallel (T026-T029)
- Tests (if included) can run in parallel within each story

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T013)
- All Foundational type definitions can run in parallel (T017-T020, T022)
- Once Foundational phase completes, User Stories 1 and 2 can start in parallel
- User Story 3 can start in parallel with US1/US2 if team capacity allows
- All MCP tools can be implemented in parallel (T059-T063)
- All chat components can be built in parallel (T078-T081)
- All polish tasks can run in parallel (T101-T116)
- All test tasks can run in parallel (T119-T128)

---

## Parallel Example: User Story 3 (Chat)

```bash
# Launch all MCP tools together:
Task T059: "Implement add_task MCP tool"
Task T060: "Implement list_tasks MCP tool"
Task T061: "Implement get_task MCP tool"
Task T062: "Implement update_task MCP tool"
Task T063: "Implement delete_task MCP tool"

# Launch all chat UI components together:
Task T078: "Create ChatSidebar component"
Task T079: "Create ChatMessage component"
Task T080: "Create ChatInput component"
Task T081: "Create ChatHistory component"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T013)
2. Complete Phase 2: Foundational (T014-T025) - CRITICAL
3. Complete Phase 3: User Story 1 - Dashboard (T026-T040)
4. Complete Phase 4: User Story 2 - Authentication (T041-T056)
5. **STOP and VALIDATE**: Test dashboard with authentication independently
6. Deploy/demo if ready - **This is a functional MVP!**

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Dashboard) → Test independently
3. Add User Story 2 (Auth) → Test independently → **Deploy/Demo (Secure MVP!)**
4. Add User Story 3 (Chat + AI) → Test independently → **Deploy/Demo (AI-powered!)**
5. Add User Story 4 (Intelligence) → Test independently → **Deploy/Demo (Full feature set!)**
6. Add Polish → Final production release

### Parallel Team Strategy

With multiple developers:

1. **Week 1**: Team completes Setup + Foundational together (T001-T025)
2. **Week 2-3**: Once Foundational is done:
   - Developer A: User Story 1 (Dashboard) - T026-T040
   - Developer B: User Story 2 (Auth) - T041-T056
   - Developer C: MCP Server setup - T057-T068
3. **Week 4-5**:
   - Developer A: Chat UI - T078-T091
   - Developer B: AI Agent - T069-T077
   - Developer C: User Story 4 - T092-T100
4. **Week 6**: Team completes Polish together (T101-T118)

---

## Task Summary

**Total Tasks**: 128 (118 implementation + 10 optional testing)

**By Phase**:
- Phase 1 (Setup): 13 tasks
- Phase 2 (Foundational): 12 tasks
- Phase 3 (US1 - Dashboard): 15 tasks
- Phase 4 (US2 - Auth): 16 tasks
- Phase 5 (US3 - Chat): 35 tasks
- Phase 6 (US4 - Intelligence): 9 tasks
- Phase 7 (Polish): 18 tasks
- Optional Testing: 10 tasks

**By User Story**:
- US1 (Dashboard): 15 tasks
- US2 (Authentication): 16 tasks
- US3 (Chat + AI): 35 tasks
- US4 (Intelligence): 9 tasks
- Infrastructure: 43 tasks
- Polish: 18 tasks

**Parallel Opportunities**: 52 tasks marked [P] can run in parallel within their phase

**MVP Scope** (Recommended): Phase 1 + Phase 2 + Phase 3 + Phase 4 = 56 tasks
- Delivers: Secure task management dashboard with full CRUD operations
- Estimated: 2-3 weeks for single developer, 1-2 weeks for team

**Full Feature Set**: All 118 implementation tasks
- Delivers: Complete AI-powered task management with natural language interface
- Estimated: 4-6 weeks for single developer, 2-3 weeks for team

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are optional but recommended for production deployment
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MCP server must be running for User Story 3 to function
- Phase 2 backend must be running for all user stories
- Environment variables must be configured before testing
