# Technology Research: AI Agent & MCP Integration

**Feature**: Phase 3 AI Agent & MCP Integration
**Date**: 2026-02-06
**Status**: Phase 0 - Technology Validation

## Overview

This document captures research findings and best practices for the technology stack selected for Phase 3. Each technology has been validated for feasibility, documented for implementation patterns, and assessed for risks and limitations.

## 1. Next.js 15+ App Router

### Overview
Next.js 15+ with App Router provides a modern React framework with server-side rendering, API routes, and file-based routing using the `app/` directory structure.

### Key Features for Phase 3
- **Route Groups**: `(auth)` and `(dashboard)` for organizing routes without affecting URL structure
- **Server Components**: Default server-side rendering for improved performance
- **API Routes**: `app/api/` directory for backend endpoints
- **Layouts**: Shared layouts for authentication and dashboard sections
- **Middleware**: Authentication checks and redirects

### Implementation Patterns

#### Route Groups
```typescript
// app/(auth)/login/page.tsx - Login page (no auth required)
// app/(dashboard)/page.tsx - Dashboard (auth required)
// app/(dashboard)/layout.tsx - Shared layout with chat sidebar
```

#### Server Actions (Optional for MVP)
```typescript
// app/actions/tasks.ts
'use server'
export async function createTask(formData: FormData) {
  // Server-side task creation
}
```

#### API Routes
```typescript
// app/api/chat/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const body = await request.json()
  // Handle chat request
  return NextResponse.json({ response: '...' })
}
```

### Best Practices
- Use Server Components by default, Client Components only when needed (interactivity, hooks)
- Implement loading.tsx and error.tsx for better UX
- Use middleware.ts for authentication checks
- Leverage parallel routes for complex layouts
- Use route handlers (API routes) for backend logic

### Limitations
- API routes have execution time limits (10s on Vercel free tier, 60s on Pro)
- Server Components cannot use React hooks or browser APIs
- Edge runtime has limited Node.js API support

### Security Considerations
- Never expose API keys in client components
- Validate all inputs in API routes
- Use CSRF protection for mutations
- Implement rate limiting on API routes

### References
- Next.js 15 Documentation: https://nextjs.org/docs
- App Router Migration Guide: https://nextjs.org/docs/app/building-your-application/upgrading/app-router-migration

## 2. Better Auth

### Overview
Better Auth is a modern, TypeScript-first authentication library for Next.js with built-in support for multiple authentication methods and database adapters.

### Key Features for Phase 3
- **Database Adapter**: PostgreSQL support via Prisma or direct SQL
- **Session Management**: JWT or database sessions
- **Multiple Auth Methods**: Email/password, OAuth providers
- **TypeScript-First**: Full type safety
- **Flexible Configuration**: Customizable auth flows

### Implementation Patterns

#### Configuration
```typescript
// lib/auth.ts
import { betterAuth } from 'better-auth'
import { Pool } from 'pg'

export const auth = betterAuth({
  database: {
    provider: 'postgresql',
    url: process.env.DATABASE_URL,
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // MVP: disable for simplicity
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
})
```

#### API Route
```typescript
// app/api/auth/[...all]/route.ts
import { auth } from '@/lib/auth'

export const { GET, POST } = auth.handler()
```

#### Client Usage
```typescript
// hooks/useAuth.ts
import { useSession } from 'better-auth/react'

export function useAuth() {
  const { data: session, status } = useSession()
  return {
    user: session?.user,
    isAuthenticated: status === 'authenticated',
    isLoading: status === 'loading',
  }
}
```

### Database Schema
Better Auth requires specific tables. For Phase 2 integration:

```sql
-- Better Auth tables (to be added via Alembic migration)
CREATE TABLE IF NOT EXISTS sessions (
  id TEXT PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS verification_tokens (
  identifier TEXT NOT NULL,
  token TEXT NOT NULL,
  expires TIMESTAMP NOT NULL,
  PRIMARY KEY (identifier, token)
);
```

### Best Practices
- Use environment variables for database connection
- Implement proper error handling for auth failures
- Use middleware for route protection
- Store minimal data in sessions (user ID, email)
- Implement logout on all devices functionality

### Limitations
- Requires database schema changes (coordinate with Phase 2)
- Session management adds database queries
- OAuth requires external provider setup

### Security Considerations
- Use HTTPS in production
- Implement rate limiting on auth endpoints
- Hash passwords with bcrypt (built-in)
- Validate email formats
- Implement CSRF protection
- Use secure session cookies (httpOnly, secure, sameSite)

### Integration with Phase 2
- Reuse existing `users` table from Phase 2
- Add Better Auth tables via Alembic migration
- Ensure user_id foreign keys reference Phase 2 users table
- JWT tokens should include user_id for Phase 2 API calls

### References
- Better Auth Documentation: https://better-auth.com/docs
- PostgreSQL Adapter: https://better-auth.com/docs/adapters/postgresql

## 3. OpenAI Agents SDK

### Overview
OpenAI Agents SDK (also known as Swarm or Assistants API) provides a framework for building AI agents that can use tools and maintain conversation context.

### Key Features for Phase 3
- **Tool Calling**: AI can invoke functions (MCP tools)
- **Conversation Context**: Maintains chat history
- **Streaming Responses**: Real-time response generation
- **Function Definitions**: Structured tool schemas

### Implementation Patterns

#### Agent Setup
```typescript
// lib/ai-agent.ts
import OpenAI from 'openai'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

export async function createChatCompletion(
  messages: Array<{ role: string; content: string }>,
  tools: Array<any>
) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages,
    tools,
    tool_choice: 'auto',
  })

  return response
}
```

#### Tool Definition
```typescript
const tools = [
  {
    type: 'function',
    function: {
      name: 'add_task',
      description: 'Create a new task for the user',
      parameters: {
        type: 'object',
        properties: {
          title: {
            type: 'string',
            description: 'The task title',
          },
          description: {
            type: 'string',
            description: 'Optional task description',
          },
        },
        required: ['title'],
      },
    },
  },
]
```

#### Chat API Route with Tool Calling
```typescript
// app/api/chat/route.ts
export async function POST(request: NextRequest) {
  const { messages } = await request.json()

  const response = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages,
    tools: mcpTools,
  })

  const message = response.choices[0].message

  // Handle tool calls
  if (message.tool_calls) {
    for (const toolCall of message.tool_calls) {
      const result = await executeMCPTool(toolCall.function.name, toolCall.function.arguments)
      // Add tool result to messages and continue conversation
    }
  }

  return NextResponse.json({ message })
}
```

### Best Practices
- Use gpt-4o-mini for cost-effective MVP
- Implement streaming for better UX
- Handle tool call errors gracefully
- Limit conversation history to last 10-20 messages
- Implement token counting to avoid context limits
- Use system prompts to guide agent behavior

### Limitations
- API rate limits (3,500 RPM for gpt-4o-mini on Tier 1)
- Token limits (128k for gpt-4o-mini)
- Cost per request ($0.150 per 1M input tokens, $0.600 per 1M output tokens)
- Tool calling adds latency
- No built-in conversation persistence

### Security Considerations
- Never expose OpenAI API key to client
- Validate tool call parameters before execution
- Implement rate limiting per user
- Sanitize user inputs to prevent prompt injection
- Log all AI interactions for debugging and safety

### Cost Optimization
- Use gpt-4o-mini instead of gpt-4o (10x cheaper)
- Limit conversation history length
- Cache system prompts
- Implement request queuing to avoid rate limits
- Monitor usage with OpenAI dashboard

### References
- OpenAI API Documentation: https://platform.openai.com/docs/api-reference
- Function Calling Guide: https://platform.openai.com/docs/guides/function-calling
- Rate Limits: https://platform.openai.com/docs/guides/rate-limits

## 4. MCP (Model Context Protocol) SDK

### Overview
MCP SDK provides a standardized protocol for exposing tools to AI agents. It defines a JSON-RPC interface for tool discovery and execution.

### Key Features for Phase 3
- **Tool Discovery**: AI agents can list available tools
- **Structured Schemas**: JSON Schema for tool inputs/outputs
- **Error Handling**: Standardized error responses
- **Stateless Design**: Each tool call is independent

### Implementation Patterns

#### MCP Server Setup
```typescript
// mcp-server/src/index.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'

const server = new Server(
  {
    name: 'phase3-task-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
)

// Register tools
server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'add_task',
        description: 'Create a new task',
        inputSchema: {
          type: 'object',
          properties: {
            title: { type: 'string' },
            description: { type: 'string' },
          },
          required: ['title'],
        },
      },
    ],
  }
})

server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params

  if (name === 'add_task') {
    return await addTask(args)
  }

  throw new Error(`Unknown tool: ${name}`)
})
```

#### Tool Implementation
```typescript
// mcp-server/src/tools/add-task.ts
import { callPhase2API } from '../client'

export async function addTask(args: { title: string; description?: string }) {
  try {
    const response = await callPhase2API('/api/tasks', {
      method: 'POST',
      body: JSON.stringify({
        title: args.title,
        description: args.description || '',
        completed: false,
      }),
    })

    return {
      content: [
        {
          type: 'text',
          text: `Task created successfully: ${response.title}`,
        },
      ],
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error creating task: ${error.message}`,
        },
      ],
      isError: true,
    }
  }
}
```

### Best Practices
- Keep tools stateless (no shared state between calls)
- Validate all inputs with JSON Schema
- Return structured error messages
- Log all tool executions
- Implement timeouts for Phase 2 API calls
- Use descriptive tool names and descriptions

### Limitations
- Requires separate server process
- JSON-RPC protocol overhead
- No built-in authentication (must implement separately)
- Tool discovery happens at runtime

### Security Considerations
- Validate all tool inputs
- Implement authentication for MCP server access
- Rate limit tool executions
- Sanitize outputs before returning to AI
- Never expose sensitive data in tool responses
- Implement audit logging for all tool calls

### Integration with OpenAI
```typescript
// Convert MCP tools to OpenAI function format
function mcpToolToOpenAIFunction(mcpTool: MCPTool) {
  return {
    type: 'function',
    function: {
      name: mcpTool.name,
      description: mcpTool.description,
      parameters: mcpTool.inputSchema,
    },
  }
}
```

### References
- MCP Specification: https://modelcontextprotocol.io/docs
- MCP SDK (TypeScript): https://github.com/modelcontextprotocol/typescript-sdk

## 5. Shadcn UI

### Overview
Shadcn UI is a collection of re-usable components built with Radix UI and Tailwind CSS. Components are copied into your project (not installed as dependency).

### Key Features for Phase 3
- **Accessible**: Built on Radix UI primitives
- **Customizable**: Full control over component code
- **TypeScript**: Full type safety
- **Tailwind CSS**: Utility-first styling
- **Dark Mode**: Built-in support

### Implementation Patterns

#### Installation
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card input textarea
```

#### Component Usage
```typescript
// components/dashboard/TaskCard.tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

export function TaskCard({ task }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{task.title}</CardTitle>
        <CardDescription>{task.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <Button onClick={() => handleComplete(task.id)}>
          Complete
        </Button>
      </CardContent>
    </Card>
  )
}
```

#### Theming
```typescript
// tailwind.config.ts
module.exports = {
  theme: {
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
      },
    },
  },
}
```

### Best Practices
- Install only components you need
- Customize components in your codebase
- Use CSS variables for theming
- Implement dark mode from the start
- Follow Radix UI accessibility guidelines

### Limitations
- Components are copied (not versioned)
- Updates require manual copying
- Requires Tailwind CSS setup
- Some components have peer dependencies

### Components for Phase 3
- **Button**: Task actions, form submissions
- **Card**: Task cards, chat messages
- **Input/Textarea**: Task forms, chat input
- **Dialog**: Task creation modal
- **Dropdown Menu**: Task actions menu
- **Badge**: Task status indicators
- **Separator**: Visual dividers
- **ScrollArea**: Chat history, task list

### References
- Shadcn UI Documentation: https://ui.shadcn.com
- Radix UI Primitives: https://www.radix-ui.com/primitives

## 6. Phase 2 API Authentication

### Overview
Phase 2 FastAPI backend uses JWT token authentication. Phase 3 frontend must obtain and include JWT tokens in all API requests.

### Authentication Flow

1. **User Login** (via Better Auth)
   - User submits credentials to Better Auth
   - Better Auth validates against Phase 2 database
   - Better Auth creates session

2. **JWT Token Generation**
   - Frontend requests JWT token from Phase 2 `/api/auth/token` endpoint
   - Phase 2 validates Better Auth session
   - Phase 2 returns JWT token

3. **API Requests**
   - Frontend includes JWT token in Authorization header
   - Phase 2 validates token on each request
   - Phase 2 returns data or error

### Implementation Patterns

#### API Client
```typescript
// lib/api-client.ts
export class Phase2APIClient {
  private baseURL: string
  private token: string | null = null

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  setToken(token: string) {
    this.token = token
  }

  async request(endpoint: string, options: RequestInit = {}) {
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
      throw new Error(`API error: ${response.statusText}`)
    }

    return response.json()
  }

  async getTasks() {
    return this.request('/api/tasks')
  }

  async createTask(task: { title: string; description: string }) {
    return this.request('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(task),
    })
  }
}
```

#### Token Management
```typescript
// hooks/useTasks.ts
import { useAuth } from './useAuth'
import { Phase2APIClient } from '@/lib/api-client'

export function useTasks() {
  const { user } = useAuth()
  const client = new Phase2APIClient(process.env.NEXT_PUBLIC_PHASE2_API_URL)

  useEffect(() => {
    if (user?.token) {
      client.setToken(user.token)
    }
  }, [user])

  // ... task operations
}
```

### Best Practices
- Store JWT token securely (httpOnly cookie or secure storage)
- Refresh tokens before expiration
- Handle 401 errors (redirect to login)
- Implement retry logic for network errors
- Use environment variables for API URL

### Security Considerations
- Never log JWT tokens
- Validate token expiration on client
- Implement token refresh mechanism
- Use HTTPS for all API calls
- Handle CORS properly

### Error Handling
```typescript
async function handleAPIError(error: any) {
  if (error.status === 401) {
    // Token expired or invalid
    redirectToLogin()
  } else if (error.status === 403) {
    // Forbidden
    showError('You do not have permission to perform this action')
  } else if (error.status === 429) {
    // Rate limited
    showError('Too many requests. Please try again later.')
  } else {
    // Generic error
    showError('An error occurred. Please try again.')
  }
}
```

### References
- Phase 2 API Documentation: `/phase-2/docs/`
- JWT Best Practices: https://tools.ietf.org/html/rfc8725

## Technology Stack Summary

| Technology | Purpose | Version | Status |
|------------|---------|---------|--------|
| Next.js | Web framework | 15+ | ✅ Validated |
| Better Auth | Authentication | Latest | ✅ Validated |
| OpenAI API | AI agent | Latest | ✅ Validated |
| MCP SDK | Tool protocol | Latest | ✅ Validated |
| Shadcn UI | UI components | Latest | ✅ Validated |
| Tailwind CSS | Styling | 3.4+ | ✅ Validated |
| TypeScript | Language | 5.3+ | ✅ Validated |
| Vitest | Unit testing | Latest | ⏳ To validate |
| Playwright | E2E testing | Latest | ⏳ To validate |

## Known Issues & Workarounds

### Issue 1: Next.js API Route Timeouts
- **Problem**: Long-running AI operations may timeout
- **Workaround**: Implement streaming responses, show progress indicators

### Issue 2: Better Auth Database Schema
- **Problem**: Requires schema changes to Phase 2 database
- **Workaround**: Create Alembic migration, coordinate with Phase 2 team

### Issue 3: MCP Server Deployment
- **Problem**: Requires separate service deployment
- **Workaround**: Use Docker Compose for local dev, document deployment options

### Issue 4: OpenAI Rate Limits
- **Problem**: API rate limits may affect user experience
- **Workaround**: Implement client-side rate limiting, queue requests

## Next Steps

1. ✅ Technology validation complete
2. ⏳ Create data-model.md with entity definitions
3. ⏳ Create contracts/ with API schemas
4. ⏳ Create quickstart.md with setup instructions
5. ⏳ Generate tasks.md with implementation tasks
