---
id: 0002
title: Phase 3 AI Agent MCP Implementation Plan
stage: plan
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5
feature: 003-ai-agent-mcp
branch: 003-ai-agent-mcp
user: amber
command: /sp.plan
labels: ["planning", "ai-agent", "mcp", "nextjs", "better-auth", "openai", "phase-3", "architecture"]
links:
  spec: /mnt/e/Hackathon-2/specs/003-ai-agent-mcp/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-ai-agent-mcp/plan.md
  - specs/003-ai-agent-mcp/research.md
  - specs/003-ai-agent-mcp/data-model.md
  - specs/003-ai-agent-mcp/contracts/mcp-tools.json
  - specs/003-ai-agent-mcp/contracts/frontend-api.md
  - specs/003-ai-agent-mcp/quickstart.md
tests:
  - None (planning phase)
---

## Prompt

Create a detailed execution plan for Phase 3: AI Agent & MCP Integration.

REQUIREMENTS:
1. Setup /phase-3 directory using Next.js 15+ (App Router), Tailwind CSS, and Shadcn UI
2. Configure Better Auth for frontend linked to existing Neon DB from Phase 2
3. Design Dashboard UI to fetch and display tasks from Phase 2 FastAPI backend
4. Setup OpenAI Agents SDK on server-side of Next.js for Chatbot logic
5. Create MCP Server within project exposing Phase 2 CRUD functions as executable tools for AI Agent
6. Implement Chat Sidebar component for natural language task management
7. Define done criteria: secure login/logout, visual dashboard, chat-based task creation

CONSTRAINTS:
- Strictly adhere to /phase-3 folder
- Ensure secure communication with /phase-2 backend
- Follow spec-driven development workflow

## Response snapshot

Created comprehensive implementation plan for Phase 3: AI Agent & MCP Integration with the following deliverables:

**plan.md** - Complete implementation plan including:
- Summary: Phase 3 adds Next.js 15+ web frontend with AI-powered task management via OpenAI Agents SDK and MCP tools
- Technical Context: TypeScript 5.3+, Node.js 18+, Next.js 15+, Better Auth, OpenAI Agents SDK, MCP SDK, Shadcn UI
- Constitution Check: All 6 gates passed (Phase Isolation, Spec-Driven Development, Scope Discipline, Protected Directories, Verification-First, Evolutionary Architecture)
- Project Structure: Detailed directory layout for /phase-3 with frontend/ (Next.js app), mcp-server/ (TypeScript MCP service), and tests/
- Architecture Decisions: 4 key decisions documented with rationale:
  - AD-001: MCP Server as Separate Service (security, separation of concerns, reusability)
  - AD-002: Better Auth with Neon PostgreSQL (single source of truth, cost efficiency)
  - AD-003: Session Storage for Chat History (MVP simplicity, evolutionary path)
  - AD-004: OpenAI Agents SDK in Next.js API Routes (security, performance, integration)
- Risks & Mitigation: 8 risks identified (3 high, 3 medium, 2 low) with mitigation strategies
- Dependencies: External services, internal dependencies, development tools, third-party libraries
- Open Questions: 6 questions with proposed resolutions

**research.md** - Technology validation and best practices for:
1. Next.js 15+ App Router (route groups, server components, API routes)
2. Better Auth setup with Neon PostgreSQL (configuration, session management, JWT)
3. OpenAI Agents SDK integration (agent creation, tool calling, streaming)
4. MCP SDK usage (server setup, tool definition, error handling)
5. Shadcn UI component library (installation, theming, customization)
6. Phase 2 API authentication (JWT token flow, error handling)

**data-model.md** - Entity definitions and relationships:
- 6 entities: User (Phase 2), Task (Phase 2), Session (Better Auth), ChatMessage (SessionStorage), MCPTool, AgentContext
- Entity relationship diagram showing 1:N relationships
- Complete TypeScript type definitions for all entities
- Validation rules and type safety strategy
- Migration considerations for future chat persistence

**contracts/mcp-tools.json** - MCP tool schemas for 5 tools:
- add_task: Create new task
- list_tasks: List tasks with filters
- get_task: Get specific task
- update_task: Update task fields
- delete_task: Delete task
- Complete JSON Schema definitions with input/output schemas, examples, error responses

**contracts/frontend-api.md** - API contracts for:
- Better Auth endpoints (sign-up, sign-in, sign-out, session)
- Chat endpoint (POST /api/chat with AI agent)
- Phase 2 backend integration (tasks CRUD endpoints)
- Error response format, rate limiting, CORS configuration, security considerations
- Client implementation examples

**quickstart.md** - Local development setup guide:
- Prerequisites verification (Node.js 18+, Phase 2 backend, OpenAI API key)
- Step-by-step setup (clone, install, configure, database migration, Shadcn UI, start servers)
- Verification steps for auth, Phase 2 integration, AI chat, MCP tools
- Common issues & solutions (5 issues with troubleshooting steps)
- Development workflow, debugging tips, useful commands
- Target setup time: <30 minutes

## Outcome

- ✅ Impact: Complete implementation plan for Phase 3 AI Agent & MCP integration, defining architecture, technology stack, data models, API contracts, and setup instructions. All planning artifacts ready for task generation.
- 🧪 Tests: No tests (planning phase)
- 📁 Files: 6 files created (plan.md, research.md, data-model.md, mcp-tools.json, frontend-api.md, quickstart.md)
- 🔁 Next prompts: `/sp.tasks` to generate actionable task list with dependencies, or `/sp.adr` if architectural decisions need formal ADR documentation
- 🧠 Reflection: Planning successfully balances technical depth (4 architecture decisions with rationale, 8 risks with mitigation) with practical guidance (quickstart in <30 minutes, troubleshooting for 5 common issues). All constitution gates passed. MCP server as separate service is key architectural decision enabling security and phase isolation. SessionStorage for chat (MVP) provides evolutionary path to database persistence.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully with all required artifacts generated
- Graders run and results (PASS/FAIL): Constitution Check - ALL PASS (6/6 gates), Planning Completeness - PASS (all required sections documented)
- Prompt variant (if applicable): Standard /sp.plan workflow with comprehensive artifact generation
- Next experiment (smallest change to try): Proceed to task generation (/sp.tasks) to validate that planning artifacts provide sufficient detail for implementation. Monitor if any gaps emerge during task breakdown that indicate planning could be improved.
