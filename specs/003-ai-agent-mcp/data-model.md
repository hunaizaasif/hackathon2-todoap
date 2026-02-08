# Data Model: AI Agent & MCP Integration

**Feature**: Phase 3 AI Agent & MCP Integration
**Date**: 2026-02-06
**Status**: Phase 1 - Design

## Overview

This document defines the data entities, their relationships, and TypeScript type definitions for Phase 3. The data model integrates with Phase 2's existing User and Task entities while introducing new entities for chat functionality and AI agent operations.

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │ (Phase 2 - existing)
│  (Phase 2)  │
└──────┬──────┘
       │
       │ 1:N
       │
       ├─────────────────┬─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│    Task     │   │   Session   │   │ChatMessage  │
│  (Phase 2)  │   │(Better Auth)│   │(SessionStorage)│
└─────────────┘   └─────────────┘   └──────┬──────┘
                                            │
                                            │ references
                                            │
                                            ▼
                                    ┌─────────────┐
                                    │  MCP Tool   │
                                    │  Execution  │
                                    └─────────────┘
```

## Core Entities

### 1. User (Phase 2 - Existing)

**Source**: Phase 2 database (`users` table)
**Ownership**: Phase 2 backend
**Access**: Read-only from Phase 3

```typescript
// types/user.ts
export interface User {
  id: string                    // UUID
  email: string                 // Unique email address
  hashed_password: string       // Bcrypt hashed password (not exposed to frontend)
  created_at: string           // ISO 8601 timestamp
  updated_at: string           // ISO 8601 timestamp
}

// Frontend-safe user type (excludes sensitive fields)
export interface UserProfile {
  id: string
  email: string
  created_at: string
}
```

**Constraints**:
- `id`: Primary key, UUID v4
- `email`: Unique, valid email format, max 255 characters
- `hashed_password`: Never exposed to frontend
- `created_at`, `updated_at`: Managed by Phase 2 backend

**Phase 3 Usage**:
- Authentication via Better Auth
- Task ownership validation
- User context for AI agent

### 2. Task (Phase 2 - Existing)

**Source**: Phase 2 database (`tasks` table)
**Ownership**: Phase 2 backend
**Access**: Read/Write via Phase 2 API

```typescript
// types/task.ts
export interface Task {
  id: string                    // UUID
  user_id: string              // Foreign key to users.id
  title: string                // Task title
  description: string          // Task description (can be empty)
  completed: boolean           // Completion status
  created_at: string          // ISO 8601 timestamp
  updated_at: string          // ISO 8601 timestamp
}

// Task creation input (frontend)
export interface CreateTaskInput {
  title: string
  description?: string
}

// Task update input (frontend)
export interface UpdateTaskInput {
  title?: string
  description?: string
  completed?: boolean
}

// Task filters (frontend)
export interface TaskFilters {
  completed?: boolean
  search?: string              // Search in title/description
  sortBy?: 'created_at' | 'updated_at' | 'title'
  sortOrder?: 'asc' | 'desc'
}
```

**Constraints**:
- `id`: Primary key, UUID v4
- `user_id`: Foreign key, must reference existing user
- `title`: Required, max 255 characters
- `description`: Optional, max 2000 characters
- `completed`: Default false
- `created_at`, `updated_at`: Managed by Phase 2 backend

**Phase 3 Usage**:
- Dashboard display and management
- AI agent task operations (via MCP tools)
- Task filtering and search

### 3. Session (Better Auth)

**Source**: Phase 3 database (`sessions` table - new)
**Ownership**: Better Auth
**Access**: Managed by Better Auth library

```typescript
// types/session.ts
export interface Session {
  id: string                    // Session ID
  user_id: string              // Foreign key to users.id
  expires_at: string           // ISO 8601 timestamp
  created_at: string           // ISO 8601 timestamp
}

// Session data exposed to frontend
export interface SessionData {
  user: UserProfile
  expiresAt: string
}
```

**Constraints**:
- `id`: Primary key, random string
- `user_id`: Foreign key, must reference existing user
- `expires_at`: Must be future timestamp
- Sessions expire after 7 days (configurable)

**Phase 3 Usage**:
- User authentication state
- JWT token generation
- Protected route access

### 4. Chat Message (SessionStorage - MVP)

**Source**: Browser SessionStorage
**Ownership**: Frontend only
**Access**: Client-side only (no backend persistence in MVP)

```typescript
// types/chat.ts
export interface ChatMessage {
  id: string                    // UUID v4 (client-generated)
  role: 'user' | 'assistant' | 'system' | 'tool'
  content: string              // Message text
  timestamp: string            // ISO 8601 timestamp
  tool_calls?: ToolCall[]      // Optional tool calls (for assistant messages)
  tool_call_id?: string        // Optional tool call ID (for tool messages)
}

export interface ToolCall {
  id: string                    // Tool call ID
  type: 'function'
  function: {
    name: string               // MCP tool name
    arguments: string          // JSON string of arguments
  }
}

// Chat conversation (stored in SessionStorage)
export interface ChatConversation {
  id: string                    // Conversation ID
  messages: ChatMessage[]
  created_at: string
  updated_at: string
}

// Chat input from user
export interface ChatInput {
  message: string
  conversationId?: string      // Optional: continue existing conversation
}

// Chat response to user
export interface ChatResponse {
  message: ChatMessage
  conversationId: string
}
```

**Constraints**:
- `id`: UUID v4, client-generated
- `role`: Must be one of: 'user', 'assistant', 'system', 'tool'
- `content`: Max 10,000 characters
- `timestamp`: ISO 8601 format
- SessionStorage limit: ~5-10MB (browser-dependent)
- Messages cleared on browser close/refresh

**Phase 3 Usage**:
- Chat interface display
- Conversation context for AI agent
- Tool call tracking

**Future Migration Path**:
```typescript
// Future: Database-persisted chat messages
export interface ChatMessageDB {
  id: string
  user_id: string              // Foreign key to users.id
  conversation_id: string      // Group messages by conversation
  role: 'user' | 'assistant' | 'system' | 'tool'
  content: string
  metadata: Record<string, any> // Tool calls, etc.
  created_at: string
}
```

### 5. MCP Tool Definition

**Source**: MCP server code
**Ownership**: MCP server
**Access**: Discovered at runtime via MCP protocol

```typescript
// types/mcp.ts
export interface MCPTool {
  name: string                  // Tool identifier (e.g., 'add_task')
  description: string           // Human-readable description
  inputSchema: {                // JSON Schema for input validation
    type: 'object'
    properties: Record<string, any>
    required?: string[]
  }
}

// MCP tool execution request
export interface MCPToolCallRequest {
  name: string                  // Tool name
  arguments: Record<string, any> // Tool arguments
}

// MCP tool execution response
export interface MCPToolCallResponse {
  content: Array<{
    type: 'text' | 'image' | 'resource'
    text?: string
    data?: string
    mimeType?: string
  }>
  isError?: boolean
}
```

**Available Tools**:
1. `add_task`: Create a new task
2. `list_tasks`: List user's tasks with optional filters
3. `get_task`: Get a specific task by ID
4. `update_task`: Update an existing task
5. `delete_task`: Delete a task

**Phase 3 Usage**:
- AI agent tool discovery
- Tool execution via MCP server
- Tool result display in chat

### 6. AI Agent Context

**Source**: Runtime state (not persisted)
**Ownership**: Next.js API route
**Access**: Server-side only

```typescript
// types/agent.ts
export interface AgentContext {
  userId: string                // Current user ID
  conversationHistory: ChatMessage[] // Recent messages
  availableTools: MCPTool[]    // Tools from MCP server
  systemPrompt: string         // Agent instructions
}

// Agent execution request
export interface AgentRequest {
  userId: string
  message: string
  conversationId?: string
}

// Agent execution response
export interface AgentResponse {
  message: ChatMessage
  conversationId: string
  toolsExecuted: string[]      // Names of tools executed
}
```

**Phase 3 Usage**:
- AI agent initialization
- Tool calling orchestration
- Conversation management

## Data Flow Diagrams

### Authentication Flow

```
User → Better Auth → Phase 2 DB (users table)
                  ↓
            Session Created
                  ↓
            JWT Token Generated
                  ↓
            Frontend Stores Token
                  ↓
            API Requests Include Token
```

### Task Management Flow (Dashboard)

```
User Action → Frontend Component → Phase 2 API Client
                                         ↓
                                   JWT Validation
                                         ↓
                                   Phase 2 Backend
                                         ↓
                                   Database (tasks table)
                                         ↓
                                   Response to Frontend
                                         ↓
                                   UI Update
```

### Chat Flow (AI Agent)

```
User Message → Chat Component → SessionStorage (save)
                              ↓
                        Next.js API Route (/api/chat)
                              ↓
                        OpenAI Agents SDK
                              ↓
                        Tool Call Detected
                              ↓
                        MCP Server
                              ↓
                        Phase 2 API
                              ↓
                        Tool Result
                              ↓
                        AI Response Generated
                              ↓
                        Response to Frontend
                              ↓
                        SessionStorage (save)
                              ↓
                        UI Update
```

## Storage Strategy

### Phase 2 Database (Neon PostgreSQL)
- **Entities**: User, Task, Session
- **Access**: Via Phase 2 API (tasks), Better Auth (sessions)
- **Persistence**: Permanent
- **Backup**: Managed by Neon

### SessionStorage (Browser)
- **Entities**: ChatMessage, ChatConversation
- **Access**: Client-side JavaScript only
- **Persistence**: Session-only (cleared on close)
- **Backup**: None (MVP limitation)

### Runtime Memory (Server)
- **Entities**: AgentContext, MCPTool definitions
- **Access**: Server-side only
- **Persistence**: None (recreated per request)
- **Backup**: N/A

## Validation Rules

### User
- Email: Valid email format, unique, max 255 chars
- Password: Min 8 chars, must include uppercase, lowercase, number (enforced by Better Auth)

### Task
- Title: Required, 1-255 chars, non-empty after trim
- Description: Optional, max 2000 chars
- Completed: Boolean only

### Chat Message
- Content: Required, 1-10000 chars
- Role: Must be 'user' | 'assistant' | 'system' | 'tool'
- Timestamp: Valid ISO 8601 format

### MCP Tool Arguments
- Validated against tool's inputSchema (JSON Schema)
- Required fields must be present
- Type checking enforced

## Type Safety Strategy

### Frontend Types
```typescript
// Strict TypeScript configuration
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

### Runtime Validation
```typescript
// Use Zod for runtime validation
import { z } from 'zod'

export const CreateTaskSchema = z.object({
  title: z.string().min(1).max(255),
  description: z.string().max(2000).optional(),
})

export const ChatMessageSchema = z.object({
  id: z.string().uuid(),
  role: z.enum(['user', 'assistant', 'system', 'tool']),
  content: z.string().min(1).max(10000),
  timestamp: z.string().datetime(),
  tool_calls: z.array(z.any()).optional(),
  tool_call_id: z.string().optional(),
})
```

### API Response Types
```typescript
// Type-safe API responses
export type APIResponse<T> =
  | { success: true; data: T }
  | { success: false; error: string; code: string }

// Usage
const response: APIResponse<Task[]> = await api.getTasks()
if (response.success) {
  // TypeScript knows response.data is Task[]
  console.log(response.data)
} else {
  // TypeScript knows response.error is string
  console.error(response.error)
}
```

## Migration Considerations

### Future: Chat Message Persistence

When migrating from SessionStorage to database:

```sql
-- New table for chat messages
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  conversation_id UUID NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system', 'tool')),
  content TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_chat_messages_user_conversation
  ON chat_messages(user_id, conversation_id, created_at);

-- New table for conversations
CREATE TABLE chat_conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_chat_conversations_user
  ON chat_conversations(user_id, updated_at DESC);
```

### Future: Task Enhancements

Potential Phase 2 schema extensions (out of scope for MVP):

```sql
-- Add due dates
ALTER TABLE tasks ADD COLUMN due_date TIMESTAMP;

-- Add priority
ALTER TABLE tasks ADD COLUMN priority TEXT CHECK (priority IN ('low', 'medium', 'high'));

-- Add tags
CREATE TABLE task_tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  tag TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Summary

**Entities Defined**: 6 (User, Task, Session, ChatMessage, MCPTool, AgentContext)
**Storage Layers**: 3 (PostgreSQL, SessionStorage, Runtime Memory)
**Type Definitions**: Complete TypeScript types for all entities
**Validation**: JSON Schema (MCP tools), Zod (runtime), TypeScript (compile-time)
**Migration Path**: Documented for chat persistence

**Next Steps**:
1. ✅ Data model complete
2. ⏳ Create contracts/mcp-tools.json
3. ⏳ Create contracts/frontend-api.md
4. ⏳ Create quickstart.md
