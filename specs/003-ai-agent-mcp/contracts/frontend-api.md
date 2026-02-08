# Frontend API Contracts: AI Agent & MCP Integration

**Feature**: Phase 3 AI Agent & MCP Integration
**Date**: 2026-02-06
**Status**: Phase 1 - Design

## Overview

This document defines the API contracts between Phase 3 frontend and backend services. It covers authentication endpoints (Better Auth), chat endpoints (AI agent), and Phase 2 backend integration.

## Base URLs

```
NEXT_PUBLIC_PHASE2_API_URL=http://localhost:8000  # Phase 2 FastAPI backend
NEXT_PUBLIC_FRONTEND_URL=http://localhost:3000     # Phase 3 Next.js frontend
```

## Authentication

All API requests (except auth endpoints) require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## 1. Better Auth Endpoints

### Base Path: `/api/auth`

Better Auth provides automatic endpoints via the catch-all route handler.

#### POST `/api/auth/sign-up`

Create a new user account.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response (Success - 201)**:
```json
{
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-02-06T10:30:00Z"
  },
  "session": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresAt": "2026-02-13T10:30:00Z"
  }
}
```

**Response (Error - 400)**:
```json
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "email": "Email already exists"
  }
}
```

**Validation Rules**:
- Email: Valid format, unique, max 255 characters
- Password: Min 8 characters, must include uppercase, lowercase, number
- Name: Optional, max 255 characters

---

#### POST `/api/auth/sign-in`

Authenticate an existing user.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (Success - 200)**:
```json
{
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-02-06T10:30:00Z"
  },
  "session": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresAt": "2026-02-13T10:30:00Z"
  }
}
```

**Response (Error - 401)**:
```json
{
  "error": "Invalid credentials",
  "code": "INVALID_CREDENTIALS",
  "message": "Email or password is incorrect"
}
```

---

#### POST `/api/auth/sign-out`

Sign out the current user.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Response (Success - 200)**:
```json
{
  "success": true,
  "message": "Signed out successfully"
}
```

---

#### GET `/api/auth/session`

Get current session information.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Response (Success - 200)**:
```json
{
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-02-06T10:30:00Z"
  },
  "session": {
    "expiresAt": "2026-02-13T10:30:00Z"
  }
}
```

**Response (Error - 401)**:
```json
{
  "error": "Unauthorized",
  "code": "UNAUTHORIZED",
  "message": "Session expired or invalid"
}
```

---

## 2. Chat Endpoints (AI Agent)

### Base Path: `/api/chat`

#### POST `/api/chat`

Send a message to the AI agent and receive a response.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "Remind me to buy milk tomorrow",
  "conversationId": "conv_123e4567-e89b-12d3-a456-426614174000",
  "conversationHistory": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you manage your tasks today?"
    }
  ]
}
```

**Request Fields**:
- `message` (required): User's message to the AI agent
- `conversationId` (optional): ID to continue existing conversation
- `conversationHistory` (optional): Recent messages for context (max 10 messages)

**Response (Success - 200)**:
```json
{
  "message": {
    "id": "msg_223e4567-e89b-12d3-a456-426614174001",
    "role": "assistant",
    "content": "I've created a task 'Buy milk' for you. Is there anything else you'd like me to help with?",
    "timestamp": "2026-02-06T10:35:00Z",
    "tool_calls": [
      {
        "id": "call_abc123",
        "type": "function",
        "function": {
          "name": "add_task",
          "arguments": "{\"title\":\"Buy milk\",\"description\":\"Reminder for tomorrow\"}"
        }
      }
    ]
  },
  "conversationId": "conv_123e4567-e89b-12d3-a456-426614174000",
  "toolsExecuted": ["add_task"]
}
```

**Response (Error - 400)**:
```json
{
  "error": "Invalid request",
  "code": "INVALID_REQUEST",
  "message": "Message is required and cannot be empty"
}
```

**Response (Error - 429)**:
```json
{
  "error": "Rate limit exceeded",
  "code": "RATE_LIMIT",
  "message": "Too many requests. Please try again in 60 seconds.",
  "retryAfter": 60
}
```

**Response (Error - 500)**:
```json
{
  "error": "AI service error",
  "code": "AI_ERROR",
  "message": "The AI service is temporarily unavailable. Please try again."
}
```

**Validation Rules**:
- Message: Required, 1-10000 characters
- ConversationHistory: Max 10 messages, each with role and content
- Rate Limit: 20 requests per minute per user

**Performance**:
- Target response time: <2s for 95% of requests
- Timeout: 30s (returns error if exceeded)
- Streaming: Not implemented in MVP (future enhancement)

---

## 3. Phase 2 Backend Integration

### Base Path: `${NEXT_PUBLIC_PHASE2_API_URL}/api`

These endpoints are provided by Phase 2 FastAPI backend. Phase 3 frontend calls them directly for task management via the dashboard UI.

#### GET `/api/tasks`

List all tasks for the authenticated user.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Query Parameters**:
- `completed` (optional): Filter by completion status (true/false)
- `skip` (optional): Number of tasks to skip (default: 0)
- `limit` (optional): Max tasks to return (default: 100, max: 100)

**Response (Success - 200)**:
```json
{
  "tasks": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "user_id": "user_123e4567-e89b-12d3-a456-426614174000",
      "title": "Buy milk",
      "description": "",
      "completed": false,
      "created_at": "2026-02-06T10:30:00Z",
      "updated_at": "2026-02-06T10:30:00Z"
    }
  ],
  "total": 1
}
```

---

#### POST `/api/tasks`

Create a new task.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Buy milk",
  "description": "Get 2% milk from the store"
}
```

**Response (Success - 201)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user_123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy milk",
  "description": "Get 2% milk from the store",
  "completed": false,
  "created_at": "2026-02-06T10:30:00Z",
  "updated_at": "2026-02-06T10:30:00Z"
}
```

**Response (Error - 400)**:
```json
{
  "detail": "Title is required"
}
```

---

#### GET `/api/tasks/{task_id}`

Get a specific task by ID.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Response (Success - 200)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user_123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy milk",
  "description": "Get 2% milk from the store",
  "completed": false,
  "created_at": "2026-02-06T10:30:00Z",
  "updated_at": "2026-02-06T10:30:00Z"
}
```

**Response (Error - 404)**:
```json
{
  "detail": "Task not found"
}
```

---

#### PUT `/api/tasks/{task_id}`

Update an existing task.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Buy organic milk",
  "description": "Get 2% organic milk from Whole Foods",
  "completed": true
}
```

**Response (Success - 200)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user_123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy organic milk",
  "description": "Get 2% organic milk from Whole Foods",
  "completed": true,
  "created_at": "2026-02-06T10:30:00Z",
  "updated_at": "2026-02-06T11:00:00Z"
}
```

---

#### DELETE `/api/tasks/{task_id}`

Delete a task.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Response (Success - 204)**:
```
No content
```

**Response (Error - 404)**:
```json
{
  "detail": "Task not found"
}
```

---

## Error Response Format

All endpoints follow a consistent error response format:

```json
{
  "error": "Error type",
  "code": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": {
    "field": "Additional context"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid input parameters |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | User lacks permission |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT` | 429 | Too many requests |
| `SERVER_ERROR` | 500 | Internal server error |
| `AI_ERROR` | 500 | AI service error |

---

## Rate Limiting

### Chat Endpoint
- **Limit**: 20 requests per minute per user
- **Response**: 429 with `retryAfter` field
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

### Phase 2 API
- **Limit**: 100 requests per minute per user (enforced by Phase 2)
- **Response**: 429 with retry-after header

---

## CORS Configuration

### Next.js API Routes
```typescript
// Automatically handled by Next.js
// No additional CORS configuration needed for same-origin requests
```

### Phase 2 API
```python
# Phase 2 backend must allow Phase 3 frontend origin
CORS_ORIGINS = [
  "http://localhost:3000",  # Local development
  "https://your-frontend-domain.com"  # Production
]
```

---

## Security Considerations

### Authentication
- All endpoints (except auth) require valid JWT token
- Tokens expire after 7 days
- Refresh tokens before expiration
- Implement logout on all devices

### Input Validation
- Validate all inputs on server-side
- Sanitize user inputs to prevent XSS
- Use parameterized queries to prevent SQL injection
- Limit request body size (max 1MB)

### Rate Limiting
- Implement per-user rate limits
- Use exponential backoff for retries
- Log rate limit violations

### Error Handling
- Never expose sensitive data in error messages
- Log errors server-side for debugging
- Return generic error messages to client
- Implement error tracking (e.g., Sentry)

---

## Client Implementation Examples

### API Client Setup

```typescript
// lib/api-client.ts
export class APIClient {
  private baseURL: string
  private token: string | null = null

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  setToken(token: string) {
    this.token = token
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers = {
      'Content-Type': 'application/json',
      ...(this.token && { Authorization: `Bearer ${this.token}` }),
      ...options.headers,
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.json()
      throw new APIError(error.message, error.code, response.status)
    }

    if (response.status === 204) {
      return null as T
    }

    return response.json()
  }
}

export class APIError extends Error {
  constructor(
    message: string,
    public code: string,
    public status: number
  ) {
    super(message)
    this.name = 'APIError'
  }
}
```

### Chat Request Example

```typescript
// hooks/useChat.ts
import { APIClient } from '@/lib/api-client'

export function useChat() {
  const client = new APIClient('/api')

  async function sendMessage(message: string, history: ChatMessage[]) {
    try {
      const response = await client.request<ChatResponse>('/chat', {
        method: 'POST',
        body: JSON.stringify({
          message,
          conversationHistory: history.slice(-10), // Last 10 messages
        }),
      })

      return response
    } catch (error) {
      if (error instanceof APIError) {
        if (error.code === 'RATE_LIMIT') {
          throw new Error('Too many requests. Please wait a moment.')
        } else if (error.code === 'AI_ERROR') {
          throw new Error('AI service is temporarily unavailable.')
        }
      }
      throw error
    }
  }

  return { sendMessage }
}
```

### Task Management Example

```typescript
// hooks/useTasks.ts
import { APIClient } from '@/lib/api-client'

export function useTasks() {
  const phase2Client = new APIClient(process.env.NEXT_PUBLIC_PHASE2_API_URL!)

  async function getTasks(filters?: { completed?: boolean }) {
    const params = new URLSearchParams()
    if (filters?.completed !== undefined) {
      params.set('completed', String(filters.completed))
    }

    const response = await phase2Client.request<{ tasks: Task[] }>(
      `/api/tasks?${params}`
    )

    return response.tasks
  }

  async function createTask(input: CreateTaskInput) {
    return phase2Client.request<Task>('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(input),
    })
  }

  async function updateTask(id: string, input: UpdateTaskInput) {
    return phase2Client.request<Task>(`/api/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(input),
    })
  }

  async function deleteTask(id: string) {
    return phase2Client.request<void>(`/api/tasks/${id}`, {
      method: 'DELETE',
    })
  }

  return { getTasks, createTask, updateTask, deleteTask }
}
```

---

## Testing Contracts

### Unit Tests
- Mock API responses for component tests
- Test error handling paths
- Validate request/response types

### Integration Tests
- Test actual API calls against local backend
- Verify authentication flow
- Test rate limiting behavior

### Contract Tests
- Validate request/response schemas match contracts
- Use tools like Pact or JSON Schema validation
- Run contract tests in CI/CD pipeline

---

## Versioning Strategy

### Current Version: v1

All endpoints are currently unversioned (v1 implicit). Future versions will use URL path versioning:

```
/api/v2/chat
/api/v2/tasks
```

### Breaking Changes
- Increment major version (v1 → v2)
- Maintain backward compatibility for 6 months
- Deprecation warnings in response headers

### Non-Breaking Changes
- Add optional fields to requests
- Add new fields to responses
- Add new endpoints
- No version increment needed

---

## Summary

**Endpoints Defined**: 11 (3 auth, 1 chat, 5 tasks, 2 utility)
**Authentication**: JWT Bearer tokens
**Rate Limiting**: 20 req/min (chat), 100 req/min (tasks)
**Error Handling**: Consistent error response format
**Security**: Input validation, CORS, rate limiting, error sanitization

**Next Steps**:
1. ✅ API contracts complete
2. ⏳ Create quickstart.md
3. ⏳ Update agent context
4. ⏳ Create PHR
